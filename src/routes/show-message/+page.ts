import type { paths } from '$lib/schema';
import type { PageLoad } from './$types';
import { createPathBasedClient } from 'openapi-fetch';

const client = createPathBasedClient<paths>({
	baseUrl: 'http://localhost:5173/'
});

export const load: PageLoad = async function () {
	const { data } = await client['/api/message/'].GET();
	return data;
};
