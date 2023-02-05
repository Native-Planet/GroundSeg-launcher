<script>
  // Tauri
  import { invoke } from '@tauri-apps/api/tauri'
  import { listen } from '@tauri-apps/api/event'

  // Svelte
  import { createEventDispatcher } from 'svelte'
  import { fade } from 'svelte/transition'

  const dispatch = createEventDispatcher()

  let repairing = false
  let progress = {}

  // Start the install process
  const repairGroundSeg = async () => {
    repairing = true

    const unlisten = await listen('progress',(event) => {
      progress = event.payload
    })

    dispatch("page",await invoke('repair'))
    unlisten()

    repairing = false
  }

</script>

{#if repairing}

  <div class="full-wrapper">
    <div class="bar-wrapper">

      <div style="width:{progress.total > 0 ? progress.downloaded/progress.total*100 : 0}%" class="bar-bg"></div>

      <div class="current-progress">
        {#if progress.downloaded == 0}
          Fetching download
        {:else if progress.downloaded == progress.total}
          Extracting..
        {:else}
          {(progress.downloaded/(1000**2)).toFixed(2)}/{(progress.total/(1000**2)).toFixed(2)} MB
        {/if}
      </div>

      {#if (progress.downloaded > 0) && (progress.downloaded < progress.total)}
        <div class="current-percent">{(progress.downloaded/progress.total*100).toFixed(0)}%</div>
      {/if}

    </div>

    <div class="current-item">Repairing {progress.num} of {progress.all}</div>

    {#if (progress.downloaded > 0) && (progress.downloaded < progress.total)}
      {#if progress.speed > (1000**2)}
        <div class="speed">{(progress.speed/(1000**2)).toFixed(2)} MB/s</div>
      {:else}
        <div class="speed">{(progress.speed/1000).toFixed(2)} KB/s</div>
      {/if}
    {/if}
  </div>

{:else}

  <button class="large-btn" on:click={repairGroundSeg}>
    Repair GroundSeg
  </button>

{/if}

<style>
  .full-wrapper {
    margin: 10px 20px 0 20px;
  }
  .bar-wrapper {
    position: relative;
    height: 24px;
    background: #ffffff2d;
    border: solid 1px white;
    border-radius: 8px;
    overflow: hidden;
  }
  .current-progress {
    position: absolute;
    left: 0;
    font-size: 12px;
    line-height: 24px;
    padding-left: 10px;
  }
  .current-percent {
    position: absolute;
    right: 0;
    font-size: 14px;
    line-height: 24px;
    padding-right: 10px;
  }
  .bar-bg {
    position: absolute;
    background:#181A21;
    left: 0;
    top: 0;
    height: 24px;
    transition: width 0.1s;
  }
  .current-item {
    font-size: 12px;
    float: left;
    padding: 8px 0 0 11px;
  }
  .speed {
    font-size: 12px;
    float: right;
    padding: 8px 11px 0 0;
  }
</style>
