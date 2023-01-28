<script>
  import { invoke } from '@tauri-apps/api/tauri'

  const get_page = async () => {
    let loc = await invoke('get_page')
    window.location.href = "/" + loc
  }
  get_page()

</script>
