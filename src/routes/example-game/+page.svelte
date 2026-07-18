<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<h1>Example game state</h1>
<pre>{JSON.stringify(data, null, 4)}</pre>
