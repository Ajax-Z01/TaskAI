<script lang="ts">
    import { Chart, Card, Button, Dropdown, DropdownItem, Popover, Tooltip } from 'flowbite-svelte';
    import { InfoCircleSolid, ChevronDownOutline, ChevronRightOutline, ArrowDownToBracketOutline } from 'flowbite-svelte-icons';
    import type { ApexOptions } from "apexcharts";
    import type { Task } from "$lib/types/task/task";
    import { fetchTasks } from "$lib/api/tasks";
    import { onMount } from 'svelte';

    let selectedPeriod = "Last 7 days";
    let isOpen = false;
    
    let tasks: Task[] = [];
    let taskStats = { Low: 0, Medium: 0, High: 0 };

    const PRIORITY_MAP: Record<number, string> = { 3: "Low", 2: "Medium", 1: "High" };
    const COLORS = { Low: '#22C55E', Medium: '#FACC15', High: '#DC2626' };

    async function fetchData() {
        try {
            let allTasks = await fetchTasks();

            const now = new Date();
            let startDate: Date;

            if (selectedPeriod === "Today") {
                startDate = new Date();
                startDate.setHours(0, 0, 0, 0);
            } else if (selectedPeriod === "Last 7 days") {
                startDate = new Date(now);
                startDate.setDate(startDate.getDate() - 7);
                startDate.setHours(0, 0, 0, 0);
            } else if (selectedPeriod === "Last 30 days") {
                startDate = new Date(now);
                startDate.setDate(startDate.getDate() - 30);
                startDate.setHours(0, 0, 0, 0);
            } else {
                startDate = new Date(0);
            }

            tasks = allTasks.filter((task: Task) => {
                const taskDate = new Date(task.updated_at);
                
                const localTaskDate = new Date(taskDate.getTime() - taskDate.getTimezoneOffset() * 60000);

                return localTaskDate >= startDate;
            });

            updateChartData();
        } catch (error) {
            console.error("Failed to fetch tasks", error);
        }
    }

    function updateChartData() {
        const priorityGroups: Record<string, { totalProgress: number; count: number }> = {
            Low: { totalProgress: 0, count: 0 },
            Medium: { totalProgress: 0, count: 0 },
            High: { totalProgress: 0, count: 0 }
        };

        tasks.forEach(task => {
            const priority = PRIORITY_MAP[task.priority] as keyof typeof priorityGroups;
            if (priority) {
                priorityGroups[priority].totalProgress += task.progress;
                priorityGroups[priority].count++;
            }
        });

        options.series = Object.keys(priorityGroups).map(key => {
            const group = priorityGroups[key as keyof typeof priorityGroups];
            return group.count ? (group.totalProgress / group.count) : 0;
        });

        taskStats = {
            Low: priorityGroups.Low.count,
            Medium: priorityGroups.Medium.count,
            High: priorityGroups.High.count
        };
    }

    const options: ApexOptions = {
        series: [0, 0, 0], 
        colors: Object.values(COLORS),
        chart: { height: '80%', width: '100%', type: 'radialBar', sparkline: { enabled: true } },
        plotOptions: {
            radialBar: {
                track: { background: '#E5E7EB', strokeWidth: '100%', margin: 5 },
                dataLabels: { show: false },
                hollow: { margin: 0, size: '32%' }
            }
        },
        labels: Object.keys(COLORS),
        legend: { show: true, position: 'bottom', fontFamily: 'Inter, sans-serif' },
        tooltip: { enabled: true, x: { show: false } },
        yaxis: { labels: { formatter: (value) => `${value.toFixed(2)}%` } }
    };

    function selectPeriod(period: string) {
        selectedPeriod = period;
        fetchData();
    }

    onMount(fetchData);
</script>

  
<section class="relative grid md:grid-cols-2 lg:grid-cols-3 p-4">
    <div class="col-span-full">
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Reports Overview</h1>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Track and analyze your task progress.</p>
    </div>
    <Card>
        <div class="flex justify-between items-start w-full">
            <div class="flex-col items-center">
                <div class="flex items-center mb-1">
                    <h5 class="text-xl font-bold text-gray-900 dark:text-white me-1">Tasks Progress</h5>
                    <InfoCircleSolid id="donut1" class="w-3.5 h-3.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white cursor-pointer ms-1" />
                    <Popover triggeredBy="#donut1" class="text-sm text-gray-500 bg-white border border-gray-200 rounded-lg shadow-xs w-72 dark:bg-gray-800">
                    <div class="p-3 space-y-2">
                        <h3 class="font-semibold text-gray-900 dark:text-white">Progress Overview</h3>
                        <p>This report shows the progress breakdown of tasks over the selected period.</p>
                    </div>
                    </Popover>
                </div>
            </div>
            <div class="flex justify-end items-center">
            <ArrowDownToBracketOutline class="w-3.5 h-3.5" />
            <Tooltip>Download CSV</Tooltip>
            </div>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <div class="grid grid-cols-3 gap-3 mb-2">
                <dl class="bg-red-50 dark:bg-gray-600 rounded-lg flex flex-col items-center justify-center h-[78px]">
                <dt class="w-8 h-8 rounded-full bg-red-100 dark:bg-gray-500 text-red-600 dark:text-red-300 text-sm font-medium flex items-center justify-center mb-1">{taskStats.High}</dt>
                <dd class="text-red-600 dark:text-red-300 text-sm font-medium">High</dd>
                </dl>
                <dl class="bg-yellow-50 dark:bg-gray-600 rounded-lg flex flex-col items-center justify-center h-[78px]">
                <dt class="w-8 h-8 rounded-full bg-teal-100 dark:bg-gray-500 text-yellow-600 dark:text-yellow-300 text-sm font-medium flex items-center justify-center mb-1">{taskStats.Medium}</dt>
                <dd class="text-yellow-600 dark:text-yellow-300 text-sm font-medium">Medium</dd>
                </dl>
                <dl class="bg-green-50 dark:bg-gray-600 rounded-lg flex flex-col items-center justify-center h-[78px]">
                <dt class="w-8 h-8 rounded-full bg-green-100 dark:bg-gray-500 text-green-600 dark:text-green-300 text-sm font-medium flex items-center justify-center mb-1">{taskStats.Low}</dt>
                <dd class="text-green-600 dark:text-green-300 text-sm font-medium">Low</dd>
                </dl>
            </div>
            <button on:click={() => (isOpen = !isOpen)} type="button" class="hover:underline text-xs text-gray-500 dark:text-gray-400 font-medium inline-flex items-center">Show more details <ChevronDownOutline class="w-2 h-2 ms-1" /> </button>
            {#if isOpen}
                <div id="more-details" class="border-gray-200 border-t dark:border-gray-600 pt-3 mt-3 space-y-2">
                <dl class="flex items-center justify-between">
                    <dt class="text-gray-500 dark:text-gray-400 text-sm font-normal">Average task completion rate:</dt>
                    <dd class="bg-green-100 text-green-800 text-xs font-medium inline-flex items-center px-2.5 py-1 rounded-md dark:bg-green-900 dark:text-green-300">
                    <svg class="w-2.5 h-2.5 me-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13V1m0 0L1 5m4-4 4 4" />
                    </svg> 57%
                    </dd>
                </dl>
                <dl class="flex items-center justify-between">
                    <dt class="text-gray-500 dark:text-gray-400 text-sm font-normal">Days until sprint ends:</dt>
                    <dd class="bg-gray-100 text-gray-800 text-xs font-medium inline-flex items-center px-2.5 py-1 rounded-md dark:bg-gray-600 dark:text-gray-300">13 days</dd>
                </dl>
                <dl class="flex items-center justify-between">
                    <dt class="text-gray-500 dark:text-gray-400 text-sm font-normal">Next meeting:</dt>
                    <dd class="bg-gray-100 text-gray-800 text-xs font-medium inline-flex items-center px-2.5 py-1 rounded-md dark:bg-gray-600 dark:text-gray-300">Thursday</dd>
                </dl>
                </div>
            {/if}
        </div>
        
        <Chart {options} class="py-6" />
        
        <div class="grid grid-cols-1 border-gray-200 border-t dark:border-gray-700 justify-between">
            <div class="flex justify-between items-center pt-5">
            <Button class="text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">
                {selectedPeriod} <ChevronDownOutline class="w-2.5 ms-1.5" />
            </Button>
            <Dropdown>
                <DropdownItem on:click={() => selectPeriod('Today')}>Today</DropdownItem>
                <DropdownItem on:click={() => selectPeriod('Last 7 days')}>Last 7 days</DropdownItem>
                <DropdownItem on:click={() => selectPeriod('Last 30 days')}>Last 30 days</DropdownItem>
            </Dropdown>                    
            <a href="/progress-report" class="uppercase text-sm font-semibold hover:text-primary-700 dark:hover:text-primary-500 px-3 py-2">
                PROGRESS REPORT <ChevronRightOutline class="w-2.5 h-2.5 ms-1.5" />
            </a>
            </div>
        </div>
    </Card>
</section>
