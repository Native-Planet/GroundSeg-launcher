<script>
  // Tauri
  import { invoke } from '@tauri-apps/api/tauri'
  //import { listen } from '@tauri-apps/api/event'

  // Components
  import Logo from '$lib/Logo.svelte'
  import Install from '$lib/Install.svelte'
  import InstallButton from '$lib/InstallButton.svelte'
  import Launcher from '$lib/Launcher.svelte'
  import Launching from '$lib/Launching.svelte'
  import Control from '$lib/Control.svelte'

/* Variables */
  let curFrame = "" // Which component to show
  let installing = false

/* Invokes */
  // Get the correct frame
  const getFrame = async () => {
    curFrame = await invoke('get_frame')
  }
  // Start the install process
  const installGroundSeg = async () => {
    installing = true
    curFrame = await invoke('install')
    installing = false
  }

  getFrame()

</script>

<!-- Logo is shown on all frames except launching -->
{#if (curFrame != "launching")}
  <Logo />
{/if}

<!-- Install Frame -->
{#if (curFrame == "install")}
  <Install>
    <InstallButton on:click={installGroundSeg} {installing} />
  </Install>
{/if}

<!-- Launcher Frame -->
{#if (curFrame == "launcher")}
  <Launcher on:click={e=>curFrame = e.detail}/>
{/if}

<!-- Launching Frame -->
{#if (curFrame == "launching")}
  <Launching on:page={e=>curFrame = e.detail}/>
{/if}

<!-- Control Frame -->
{#if (curFrame == "control")}
  <Control />
{/if}
