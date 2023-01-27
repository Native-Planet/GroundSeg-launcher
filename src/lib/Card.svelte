<script>
  import { fade } from 'svelte/transition'

	export let width
</script>

<div in:fade={{duration:200, delay: 160}} out:fade={{duration:200}} class="card" style="width:{width}">
	<slot/>
</div>

<style>

	.card::-webkit-scrollbar {display: none;}
	.card {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #fff;
    
    border-radius: 20px;

    background: #6d6d6d33;
    backdrop-filter: blur(20px);
    -moz-backdrop-filter: blur(20px);
    -o-backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    -ms-overflow-style: none;
		scrollbar-width: none;

    overflow: scroll;

    padding: 20px;
	}

</style>
