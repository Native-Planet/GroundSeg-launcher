<script>
  import Fa from 'svelte-fa'
  import { faCaretLeft, faCaretRight } from '@fortawesome/free-solid-svg-icons'
</script>
<div class="wrapper">
  <div class="l-icon icon">
    <Fa icon={faCaretLeft} size="2x" />
  </div>
  <img src="placeholder-slide.png" />
  <div class="r-icon icon">
    <Fa icon={faCaretRight} size="2x" />
  </div>
</div>

<style>
  .wrapper {
    width: 100%;
    display: flex;
    align-items: center;
    height: calc(100vh - 160px);
  }
  .icon {
    flex: 1;
    color: white;
    text-align: center;
  }
  img {
    border-radius: 24px;
    height: 100%;
    width: 80%;
    flex: 16;
  }
</style>
