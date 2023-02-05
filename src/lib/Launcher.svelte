<script>
  import { invoke } from '@tauri-apps/api/tauri'
  //import { listen } from '@tauri-apps/api/event'
  import { onMount, createEventDispatcher } from 'svelte'
  import { fade } from 'svelte/transition'

  import Fa from 'svelte-fa'
  import { faArrowRotateLeft } from '@fortawesome/free-solid-svg-icons'

  // Components
  import Slider from '$lib/Slider.svelte'
  import StartButton from '$lib/StartButton.svelte'

  const dispatch = createEventDispatcher()

	let ramVal = 4
  let maxRam = 4
	let cpuVal = 0
  let maxCpu = 1
  let launcherView = false
  let showRamSlider = true
  let showCpuSlider = true

  const getRam = async () => {
    ramVal = parseInt(await invoke('get_ram'))
  }

  const resetRam = async () => {
    showRamSlider = false
    ramVal = parseInt(await invoke('reset_ram'))
    showRamSlider = true
  }

  const getMaxRam = async () => {
    maxRam = parseInt(await invoke('get_max_ram'))
  }

  const getCpu = async () => {
    cpuVal = parseInt(await invoke('get_cpu'))
  }

  const resetCpu = async () => {
    showCpuSlider = false
    cpuVal = parseInt(await invoke('reset_cpu'))
    showCpuSlider = true
  }

  const getMaxCpu = async () => {
    maxCpu = parseInt(await invoke('get_max_cpu'))
  }

  onMount(async ()=> {
    await getRam()
    await getMaxRam()
    await getCpu()
    await getMaxCpu()
    launcherView = true
  })

</script>

{#if launcherView}
  <!-- Wrap all the options -->
  <div class="launcher-wrapper"
    in:fade={{duration:200, delay: 200}}
    out:fade={{duration:160}}>
    <!-- RAM -->
    <div class="launcher-item">
      <div class="launcher-title">
        <div class="launcher-text">
          Maximum RAM Usage (GB)
        </div>
        <button on:click={resetRam} class="reset-button">
          <Fa icon={faArrowRotateLeft} size="1x" />
          Default
        </button>
      </div>
      {#if showRamSlider}
      <Slider 
        on:change={(e) => ramVal = e.detail.value}
        min={4}
        max={maxRam}
        initialValue={ramVal}
        />
      {/if}
    </div>
    <!-- CPU Cores -->
    <div class="launcher-item">
      <div class="launcher-title">
        <div class="launcher-text">
          Maximum CPU Cores
        </div>
        <button on:click={resetCpu} class="reset-button">
          <Fa icon={faArrowRotateLeft} size="1x" />
          Default
        </button>
      </div>
      {#if showCpuSlider}
      <Slider 
        on:change={(e) => cpuVal = e.detail.value}
        min={1}
        max={maxCpu}
        initialValue={cpuVal}
        />
      {/if}
    </div>
    <!-- Max Storage (removed temporarily)
      
    <div class="launcher-item">
      <div class="launcher-text">
        Maximum GroundSeg VM Storage Allowed
      </div>
      <div class="launcher-storage-val">80 GB</div>
    </div>
    -->
    <div class="launcher-item">
      <div class="launcher-title">
        <div class="launcher-text">
          Give Admin Privileges to GroundSeg
        </div>
      </div>
      <StartButton
        {cpuVal} {ramVal}
        on:click={e=>dispatch('click',e.detail)}
        />
    </div>
  </div>
{/if}
