<script>
  // Tauri
  import { invoke } from '@tauri-apps/api/tauri'

  // Svelte
  import { createEventDispatcher } from 'svelte'
  import { fade } from 'svelte/transition'

  export let ramVal
  export let cpuVal

  let adminError
  let pwd = ''

  const dispatch = createEventDispatcher()

  // Launch GroundSeg VM
  const startGroundSeg = async () => {
    let res = await invoke('start', {pwd:pwd,ram:ramVal,cpu:cpuVal})
    if (res === "error") {
      console.log(res)
      adminError = true 
      setTimeout(()=>{adminError = false; pwd = ''}, 3000)
    } else {
      dispatch('click',res)
    }
  }


</script>

<input class="admin-pwd" class:admin-err={adminError} disabled={adminError} type="password" placeholder="Your Device Password" bind:value={pwd} />

<button class="start-btn {adminError ? "start-err" : pwd.length > 0 ? "start-enabled" : "start-disabled"}"
  in:fade={{delay:100,duration:160}}
  on:click={startGroundSeg}>
  {adminError ? "Incorrect Password!" : "Start GroundSeg"}
</button>
