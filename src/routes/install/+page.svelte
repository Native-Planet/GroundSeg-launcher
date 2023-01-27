<script>
  import SlideShow from '$lib/SlideShow.svelte'

  const installGroundSeg = () => {
    //window.location.href = '/installing'
    console.log("yeet")
  }
</script>

<img class="logo" src="nplogo.svg" />
<SlideShow />
<div class="l-third">
  <button on:click={installGroundSeg}>Install GroundSeg</button>
</div>

<style>
  .logo {
    height: 32px;
    padding: 14px;
  }
  .l-third {
    width: 100vw;
    background-color: #181a21;
    height: 100px;
    position: absolute;
    bottom: 0;
  }
  button {
    margin-top: 28px;
    font-family: inherit;
    border-radius: 16px;
    border: solid 1px white;
    color: inherit;
    background: none;
    width: 240px;
    line-height: 40px;
  }
  button:hover {
    background: var(--action-color);
    border-color: var(--action-color);
  }
  button:active {
    opacity: 0.6;
  }

</style>
