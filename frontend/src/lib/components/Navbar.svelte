<script>
    import { page } from '$app/stores';
    import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Avatar, Dropdown, DropdownItem, DropdownHeader, DropdownDivider } from 'flowbite-svelte';
    import { DarkMode } from 'flowbite-svelte';
    
    $: activeUrl = $page.url.pathname;

    let activeClass = 'text-primary-600 font-semibold border-b-2 border-primary-600 pb-2';
    let nonActiveClass = 'text-gray-600 dark:text-gray-300 hover:text-primary-600 transition duration-300';
</script>

<Navbar class="bg-white dark:bg-gray-900 shadow-md px-4 py-3 border-b border-gray-300 dark:border-gray-700">
    <NavBrand href="/" class="flex items-center space-x-2">
        <img src="/images/taskai-logo.svg" class="h-10 hidden md:block invert-0 dark:invert-100" alt="TaskAI Logo" />
        <span class="text-2xl font-bold text-gray-800 dark:text-white">TaskAI</span>
    </NavBrand>
    
    <div class="flex items-center md:order-2">
        <DarkMode class="mr-4 cursor-pointer" />
        <Avatar id="avatar-menu" src="/images/user-avatar.webp" class="border-2 bg-white dark:bg-white border-gray-300 dark:border-gray-700 hover:border-primary-600 transition duration-300" />
        <NavHamburger class="md:hidden text-gray-800 dark:text-white hover:text-primary-600 transition duration-300" />
    </div>

    <Dropdown placement="bottom-end" triggeredBy="#avatar-menu" class="w-56 shadow-lg rounded-lg bg-white dark:bg-gray-800 border dark:border-gray-700">
        <DropdownHeader class="p-3 dark:border-gray-700">
            <span class="block text-sm font-semibold text-gray-900 dark:text-white">User1</span>
            <span class="block truncate text-xs text-gray-500">user1@example.com</span>
        </DropdownHeader>
    
        <DropdownItem href="/" class="flex items-center gap-2 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all rounded-md">
            <i class="fas fa-chart-line text-gray-600 dark:text-gray-400"></i>
            <span>Dashboard</span>
        </DropdownItem>
    
        <DropdownItem href="/settings" class="flex items-center gap-2 p-3 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all rounded-md">
            <i class="fas fa-cog text-gray-600 dark:text-gray-400"></i>
            <span>Settings</span>
        </DropdownItem>
    
        <DropdownDivider class="my-1 border-gray-300 dark:border-gray-600" />
    
        <DropdownItem href="/logout" 
            class="flex items-center gap-2 p-3 text-red-600 hover:bg-red-100 dark:text-red-400 dark:hover:bg-red-900 transition-all rounded-md">
            <i class="fas fa-sign-out-alt"></i>
            <span>Sign Out</span>
        </DropdownItem>
    </Dropdown>    

    <NavUl {activeUrl} {activeClass} {nonActiveClass} class="md:flex space-x-6 cursor-pointer">
        <NavLi href="/">
            Home
        </NavLi>
        <NavLi href="/tasks">
            Tasks
        </NavLi>
        <NavLi href="/reports">
            Reports
        </NavLi>
        <NavLi href="/settings">
            Settings
        </NavLi>
    </NavUl>
</Navbar>
