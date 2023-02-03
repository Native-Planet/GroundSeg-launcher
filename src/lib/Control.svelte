<script>
  import { invoke } from '@tauri-apps/api/tauri'
  //import { listen } from '@tauri-apps/api/event'
  import { onMount, createEventDispatcher } from 'svelte'
  import { fade } from 'svelte/transition'

  //import Fa from 'svelte-fa'
  //import { faArrowRotateLeft } from '@fortawesome/free-solid-svg-icons'

  // Components

  const dispatch = createEventDispatcher()


  let controlView = false
  let hostname = ''
  let pwd = ''

  onMount(async ()=> {
    hostname = await invoke('get_hostname')
    controlView = true
  })

  const stopGroundSeg = () => {
    console.log("stop groundseg")
    // prompt for sudo password
  }

  const restartGroundSeg = () => {
    console.log("restart groundseg")
    // prompt for sudo password
  }

</script>

{#if controlView}
  <div class="control-wrapper"
    in:fade={{duration:200, delay: 200}}
    out:fade={{duration:160}}>
    <a 
      class="pop-open"
      target="_blank"
      href={hostname}>
      Open GroundSeg WebUI
    </a>
    <div class="admin-panel">
      <div class="admin-title">Admin Settings</div>
      <input class="admin-password" 
             type="password"
             placeholder="Your Device Password" 
             bind:value={pwd} />
      <div class="control-buttons" class:disabled={pwd.length < 1}>
        <button class="ctrl-btn stop" on:click={stopGroundSeg}>
          Stop GroundSeg
        </button>
        <button class="ctrl-btn restart" on:click={restartGroundSeg}>
          Restart GroundSeg
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .control-wrapper {
    margin: 80px;
    margin-top: 40px;
    display: flex;
    flex-direction: column;
    gap: 40px;
  }
  .control-buttons {
    display: flex; 
    gap: 12px;
  }
  .ctrl-btn {
    flex: 1;
    border: solid 1px white;
    border-radius: 12px;
    font-size: 14px;
    background: none;
    font-family: inherit;
    line-height: 48px
  }
  .ctrl-btn:active {
    opacity: .6;
  }
  .stop {
    color: red;
    border-color: red;
  }
  .disabled {
    pointer-events: none;
    opacity: .2;
  }
  .restart {
    color: orange;
    border-color: orange;
  }
  .stop:hover {
    color: white;
    background: red;
    cursor: pointer;
  }
  .restart:hover {
    color: white;
    background: orange;
    cursor: pointer;
  }
  .pop-open {
    text-decoration: none;
    border: solid 1px lime;
    font-size: 16px;
    border-radius: 16px;
    line-height: 62px;
    color: lime;
  }
  .pop-open:hover {
    color: white;
    background: lime;
  }
  .pop-open:active {
    opacity: .6;
  }
  .admin-panel {
    background: #20232c;
    padding: 20px;
    border-radius: 20px;
  }
  .admin-title {
    font-size: 14px;
    margin: 12px;
  }
  .admin-password {
    display: block;
    margin: auto;
    margin-bottom: 12px;
    margin-top: 18px;
    padding: 8px;
    width: 360px;
    text-align: center;
    color: white;
    background: #181A21;
    border: solid 1px grey;
    border-radius: 6px;
    font-family: inherit;
  }
  .admin-password::placeholder {
    color: grey;
    font-family: inherit;
  }
  .admin-password:focus {
    outline: none;
  }
</style>
