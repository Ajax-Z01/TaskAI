<script>
	import { page } from '$app/stores';
	import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper } from 'flowbite-svelte';
	import { ChartPieSolid, ClipboardListSolid, FileInvoiceOutline, CogSolid, ArrowRightToBracketOutline } from 'flowbite-svelte-icons';

	$: activeUrl = $page.url.pathname;

	let activeClass = 'flex items-center p-3 text-base font-medium text-primary-700 bg-primary-100 border-l-4 border-primary-600 rounded-md dark:text-primary-400 dark:bg-primary-900 shadow-sm';
	let nonActiveClass = 'flex items-center p-3 text-base font-normal text-gray-700 dark:text-gray-300 rounded-md hover:bg-primary-50 dark:hover:bg-gray-700 transition-all duration-300';
</script>

<Sidebar {activeUrl} {activeClass} {nonActiveClass} class="bg-white dark:bg-gray-900 shadow-md w-64 p-4 hidden md:flex flex-col border-r border-gray-300 dark:border-gray-700">
	<SidebarWrapper divClass="bg-white dark:bg-gray-900">
		<SidebarGroup>
			<SidebarItem href="/" label="Dashboard">
				<svelte:fragment slot="icon">
					<ChartPieSolid class="w-6 h-6" />
				</svelte:fragment>
			</SidebarItem>

			<SidebarItem href="/tasks" label="Tasks">
				<svelte:fragment slot="icon">
					<ClipboardListSolid class="w-6 h-6" />
				</svelte:fragment>
			</SidebarItem>

			<SidebarItem href="/reports" label="Reports">
				<svelte:fragment slot="icon">
					<FileInvoiceOutline class="w-6 h-6" />
				</svelte:fragment>
			</SidebarItem>

			<SidebarItem href="/settings" label="Settings">
				<svelte:fragment slot="icon">
					<CogSolid class="w-6 h-6" />
				</svelte:fragment>
			</SidebarItem>
		</SidebarGroup>

	</SidebarWrapper>
	<!-- Group Logout -->
	<SidebarGroup border class="pt-4 mt-auto border-t border-gray-300 dark:border-gray-700">
		<SidebarItem href="/logout" label="Sign Out">
			<svelte:fragment slot="icon">
				<ArrowRightToBracketOutline class="w-6 h-6 text-red-600 dark:text-red-400 group-hover:text-red-800 dark:group-hover:text-red-300 transition-all" />
			</svelte:fragment>
		</SidebarItem>
	</SidebarGroup>
</Sidebar>
