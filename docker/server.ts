import { $, type ServerWebSocket, type Subprocess } from 'bun'
import fs from 'fs';
import util from 'util';

/** These sockets will receive any changes to the server state */
const sockets = new Set<ServerWebSocket<unknown>>()
/** Port for webserver */
const PORT = parseInt(process.env['PORT']!) || 6543
/** Public URL for webserver, if proxied through Docker for example */
const PUBLIC_URL = process.env['PUBLIC_URL'] || 'http://localhost:' + PORT

/** Read and write file */
const readFile = util.promisify(fs.readFile);
const writeFile = util.promisify(fs.writeFile);

/** overwrite config */
async function overwriteConfig(file_path: string, target: string, replacement: string) {
  const data = await readFile(file_path, 'utf-8');
  const lines = data.split('\n');
  const updatedLines = lines.map(line => line.trim() === target ? replacement : line);
  const updatedData = updatedLines.join('\n');
  await writeFile(file_path, updatedData, 'utf-8');
}

Bun.serve({
  port: PORT,
  async fetch(req, server) {
    if (server.upgrade(req)) return

    // Application frontend
    const url = new URL(req.url)
    if (!url.pathname.startsWith('/api'))
      return new Response(Bun.file('./index.html'))

    if (url.pathname.startsWith('/api/set')) return set(await req.json())

    const cmd = url.searchParams.get('cmd')
    const sub = (url.searchParams.get('sub') as 'spigot' | 'bungee') || 'spigot'

    // Custom commands
    if (cmd === 'reset') return reset()
    if (cmd === 'start') return start(sub)
    if (cmd === 'stop') return stop(sub)

    // Any other command
    if (cmd) return command(cmd, sub)

    console.log('🔴 Not found:', url.pathname)

    return Response.json({ message: 'Not found' }, { status: 404 })
  },
  websocket: {
    open(ws) {
      // Sync the initial state
      ws.sendText(
        JSON.stringify(
          Object.fromEntries(
            Object.entries(state).filter(([k]) => interesting.includes(k))
          )
        )
      )

      // Sync further changes
      sockets.add(ws)

      // The first client initializes the server
      // if (state.spigotStatus === 'init' && state.spigotURL) {
      //   console.log('📦 Initialize spigot')
      //   spawn('spigot')
      // }
      // if (state.bungeeStatus === 'init' && state.bungeeURL) {
      //   console.log('📦 Initialize bungee')
      //   spawn('bungee')
      // }
    },
    // this is called when a message is received
    async message(ws, message) {
      console.log('📦 ' + `Received ${message}`)
    },
  },
})
console.log('📦 EaglerCraft control panel is listening on', PUBLIC_URL)

/** Server state */
const _state: {
  bungee?: Subprocess<'pipe', 'pipe', 'pipe'>
  bungeeLog: string
  bungeeStatus: 'init' | 'starting' | 'started' | 'stopping' | 'stopped'
  bungeeURL: string
  bungeeCommand: string[]
  spigot?: Subprocess<'pipe', 'pipe', 'pipe'>
  spigotLog: string
  spigotStatus: 'init' | 'starting' | 'started' | 'stopping' | 'stopped'
  spigotURL: string
  spigotCommand: string[]
} = {
  bungeeLog: '',
  bungeeStatus: 'init',
  bungeeURL:
    'https://api.papermc.io/v2/projects/waterfall/versions/1.20/builds/556/downloads/waterfall-1.20-556.jar',
  bungeeCommand: ['/usr/bin/java', '-Xms64M', '-Xmx64M', '-jar', 'bungee.jar'],
  spigotLog: '',
  spigotStatus: 'init',
  spigotURL:
    'https://cdn.getbukkit.org/spigot/spigot-1.8.8-R0.1-SNAPSHOT-latest.jar',
  spigotCommand: ['/usr/bin/java', '-Xms2G', '-Xmx2G', '-jar', 'spigot.jar'],
}

/** Properties of server state that are interesting for clients */
const interesting = [
  'bungeeCommand',
  'bungeeLog',
  'bungeeStatus',
  'bungeeURL',
  'spigotCommand',
  'spigotLog',
  'spigotStatus',
  'spigotURL',
]

/** Sync any changes to the server state to all clients */
const state = new Proxy(_state, {
  set(target, prop, value) {
    if (interesting.includes(prop as string)) {
      sockets.forEach((ws) => ws.sendText(JSON.stringify({ [prop]: value })))
    }
    // @ts-expect-error
    target[prop] = value
    return true
  },
})

/** Properties of server state that are interesting for clients */
const settable = [
  'bungeeCommand',
  'bungeeLog',
  'bungeeURL',
  'spigotCommand',
  'spigotLog',
  'spigotURL',
]

/** Update server state */
async function set(data: Partial<typeof state>) {
  // ignore if data contains unsettable properties
  if (Object.keys(data).some((k) => !settable.includes(k))) {
    return Response.json({ message: 'Invalid properties' }, { status: 400 })
  }

  Object.assign(state, data)
  return Response.json({ message: 'ok' })
}

/**
 * Send a command to a process
 * Defaults to spigot
 */
async function command(cmd: string, sub: 'spigot' | 'bungee' = 'spigot') {
  if (state[`${sub}Status`] !== 'started') {
    state[`${sub}Log`] += '🔴 Ignored ' + sub + ': ' + cmd + '\n'
    return Response.json({ message: sub + ' is not started' })
  }

  state[`${sub}Log`] += '> ' + cmd + '\n'

  state[sub]?.stdin.write(cmd + '\n')

  return Response.json({ message: 'ok' })
}

async function start(sub: 'spigot' | 'bungee') {
  state[`${sub}Log`] += '> start\n'
  spawn(sub)

  return Response.json({ message: 'starting' })
}

async function spawn(sub: 'spigot' | 'bungee') {
  if (state[`${sub}Status`] === 'starting')
    return console.error('🔴 Already starting', sub)
  if (state[`${sub}Status`] === 'started')
    return console.error('🔴 Already started', sub)
  if (state[`${sub}Status`] === 'stopping')
    return console.error('🔴 Wait for stopping', sub)

  const url = state[`${sub}URL`]
  if (!url) return console.error('🔴 No URL for', sub)

  state[`${sub}Status`] = 'starting'

  // Prepare folder and change config files
  await $`mkdir -p ${sub}`.quiet()

  if (sub === 'spigot') {
    await $`echo "eula=true" > ${sub}/eula.txt`.quiet()
    await overwriteConfig(`${sub}/server.properties`, "online-mode=true", "online-mode=false");
    await overwriteConfig(`${sub}/spigot.yml`,  "bungeecord: false", "bungeecord: true");
  }

  if (sub === 'bungee') {
    await overwriteConfig(`${sub}/config.yml`, "online_mode: true", "online_mode: false");
    await overwriteConfig(`${sub}/config.yml`, "ip_forward: false", "ip_forward: true");
    await overwriteConfig(`${sub}/plugins/EaglercraftXBungee/authservice.yml`, "enable_authentication_system: true", "enable_authentication_system: false");
    await overwriteConfig(`${sub}/plugins/EaglercraftXBungee/settings.yml`, "server_name: 'EaglercraftXBungee Server'", "server_name: 'AutoEagler Server'");
    await overwriteConfig(`${sub}/plugins/EaglercraftXBungee/listeners.yml`, "&6An EaglercraftX server", "&6An AutoEagler server");
  }

  // Generate a unique filename for the jar
  const jar = sub + '-' + Bun.hash(url).toString(36) + '.jar'
  // Download the jar if it's not already downloaded
  const downloaded = await $`wget -nv -c ${url} -O ${sub}/${jar}`.quiet()

  // Show download confirmation
  const stderr = downloaded.stderr.toString()
  if (stderr.includes('] -> "' + sub + '/' + sub + '-')) {
    console.log('🟢 Downloaded', sub, url)
  } else if (!stderr) {
    console.log('🟢 Already downloaded', sub, url)
  } else {
    console.log('🔴 Tried to download', sub, url)
    console.log(downloaded.stderr.toString())
    console.log(downloaded.stdout.toString())
  }

  // Spawn the subprocess
  const command = state[`${sub}Command`]
  const subprocess = Bun.spawn(command.slice(0, -1).concat([jar]), {
    stdin: 'pipe',
    stdout: 'pipe',
    stderr: 'pipe',
    cwd: process.cwd() + '/' + sub,
  })
  state[sub] = subprocess

  handleLines(
    sub,
    subprocess.stdout,
    sub === 'spigot' ? interpretSpigot : interpretBungee
  )
  handleLines(
    sub,
    subprocess.stderr,
    sub === 'spigot' ? interpretSpigot : interpretBungee
  )
}

async function handleLines(
  sub: 'spigot' | 'bungee',
  stream: ReadableStream<Uint8Array>,
  callback: (line: string) => void
) {
  const reader = stream.getReader()
  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const colored = new TextDecoder().decode(value)
      // Show output in the console
      // process.stdout.write('📦 ' + colored)

      // Try to interpret the output
      const text = removeShellColors(colored)
      text.split('\n').forEach(callback)

      // Sync log to the frontend
      state[`${sub}Log`] += text
    }
    console.error(`🔴 ${sub} stdout stopped`)
  } catch (error) {
    console.error(`🔴 ${sub} stdout error`, error)
  }
  state[`${sub}Status`] = 'stopped'
}

function interpretSpigot(text: string) {
  if (text.includes('\n')) return text.split('\n').forEach(interpretSpigot)
  if (!text.trim()) return

  // ! For help, type "help" or "?"
  if (text.includes('For help, type "help" or "?"'))
    state.spigotStatus = 'started'
  if (text.includes('] Stopping server')) state.spigotStatus = 'stopped'
  if (text.includes(': Stopping server')) state.spigotStatus = 'stopped'
}

function interpretBungee(text: string) {
  if (text.includes('\n')) return text.split('\n').forEach(interpretBungee)
  if (!text.trim()) return

  if (text.includes('Listening on')) state.bungeeStatus = 'started'
  if (text.includes('Closing listener')) state.bungeeStatus = 'stopped'
}

async function stop(sub: 'spigot' | 'bungee') {
  if (state[`${sub}Status`] === 'init')
    return Response.json({ message: 'Server is not started' })
  if (state[`${sub}Status`] === 'stopping')
    return Response.json({ message: 'Already stopping' })
  if (state[`${sub}Status`] === 'stopped')
    return Response.json({ message: 'Already stopped' })
  if (state[`${sub}Status`] === 'starting')
    return Response.json({ message: 'Wait for starting' })

  if (sub === 'spigot') command('stop', sub)
  else state[sub]?.kill()

  return Response.json({ message: 'Stopped' })
}

async function reset() {
  // if (state.spigotStatus !== 'stopped') await command('stop')

  // await new Promise((resolve) => setTimeout(resolve, 1000))
  // state.spigotStatus = 'stopping'

  // // send SIGHUP to the process
  // state.spigot?.kill(1)

  // console.log('stopeed', state.spigot?.exitCode, await state.spigot?.exited)
  // state.spigotStatus = 'stopped'

  // setTimeout(() => {
  //   console.log('📦 reset')
  //   process.exit(0)
  // }, 100)
  return Response.json({ message: 'Reset' })
}

function removeShellColors(input: string): string {
  return input.replace(/\x1B\[\d+m/g, '') // Regular expression to match ANSI escape codes for colors
}

// before exit
process.once('beforeExit', (code) => {
  console.log('📦 Process beforeExit event with code: ', code)
  state.spigot?.kill()
  state.bungee?.kill()
})

// Listen for termination signals allows Ctrl+C in docker run
process.on('SIGINT', () => {
  console.log('📦 Received SIGINT')
  state.spigot?.kill()
  state.bungee?.kill()
  setTimeout(() => {
    process.exit(0)
  }, 1000)
})
process.on('SIGTERM', () => {
  console.log('📦 Received SIGTERM')
  process.exit(0)
})
