<script>
  // Tauri
  import { invoke } from '@tauri-apps/api/tauri'

  // Components
  import Logo from '$lib/Logo.svelte'
  import InstallButton from '$lib/InstallButton.svelte'
  import RepairButton from '$lib/RepairButton.svelte'

  import Install from '$lib/Install.svelte'
  import Repair from '$lib/Repair.svelte'
  import Launcher from '$lib/Launcher.svelte'
  import Launching from '$lib/Launching.svelte'
  import Control from '$lib/Control.svelte'

  let curFrame = "" // Which component to show

  // Get the correct frame
  const getFrame = async () => {
    curFrame = await invoke('get_frame')
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
    <InstallButton on:page={e=>curFrame = e.detail}/>
  </Install>
{/if}

<!-- Repair Frame -->
{#if (curFrame == "fix")}
  <Repair>
    <RepairButton on:page={e=>curFrame = e.detail}/>
  </Repair>
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
  <Control on:page={e=>curFrame = e.detail}/>
{/if}
