<script lang="ts">
  import type { PageProps } from './$types'

  let { data }: PageProps = $props()
</script>

<h1>Message</h1>
<p>{data.message}</p>
