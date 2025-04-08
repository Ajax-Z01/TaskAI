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
    let completedCount = 0;
    let averageProgress = 0;
    
    $: latestTasks = [...tasks].sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()).slice(0, 5);

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
            updateTrendChart()
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
        
        completedCount = tasks.filter(task => task.progress === 100).length;
        const totalProgress = tasks.reduce((acc, t) => acc + t.progress, 0);
        averageProgress = tasks.length ? totalProgress / tasks.length : 0;
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
    
    const trendOptions: ApexOptions = {
        series: [],
        chart: {
            type: 'line',
            height: 250,
            zoom: { enabled: false },
            toolbar: { show: false },
            fontFamily: 'Inter, sans-serif',
        },
        stroke: { curve: 'smooth' },
        xaxis: {
            categories: [],
            labels: { rotate: -45 },
        },
        yaxis: {
            min: 0,
            max: 100,
            labels: { formatter: val => `${val}%` },
        },
        dataLabels: { enabled: false },
        colors: ['#3B82F6'],
        tooltip: { y: { formatter: val => `${val.toFixed(2)}%` } },
    };
    
    function updateTrendChart() {
        const trendMap: Record<string, { total: number; count: number }> = {};

        const today = new Date();
        for (let i = 6; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(today.getDate() - i);
            const key = date.toISOString().split('T')[0];
            trendMap[key] = { total: 0, count: 0 };
        }

        tasks.forEach(task => {
            const date = new Date(task.updated_at);
            const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
            const key = localDate.toISOString().split('T')[0];

            if (trendMap[key]) {
                trendMap[key].total += task.progress;
                trendMap[key].count += 1;
            }
        });

        const categories = Object.keys(trendMap);
        const seriesData = categories.map(date => {
            const entry = trendMap[date];
            return entry.count > 0 ? entry.total / entry.count : 0;
        });

        const maxY = Math.ceil(Math.max(...seriesData, 10) / 10) * 10;

        trendOptions.series = [{ name: 'Avg Progress', data: seriesData }];
        trendOptions.xaxis = { ...trendOptions.xaxis, categories };
        trendOptions.yaxis = { ...trendOptions.yaxis, max: maxY };
    }

    function selectPeriod(period: string) {
        selectedPeriod = period;
        fetchData();
    }

    onMount(fetchData);
</script>

<div class="col-span-full p-4 pb-0">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Reports Overview</h1>
    <p class="text-gray-600 dark:text-gray-300 mb-4">Track and analyze your task progress.</p>
</div>

<section class="relative grid md:grid-cols-2 lg:grid-cols-3 p-4">
    <Card>
        <div class="text-sm text-gray-400">📅 Most Active Day</div>
        <div class="text-lg font-bold">Wednesday</div>
    </Card>
    <Card>
        <div class="text-sm text-gray-400">✅ Tasks Completed</div>
        <div class="text-lg font-bold">{completedCount}</div>
    </Card>
    <Card>
        <div class="text-sm text-gray-400">📈 Avg. Progress</div>
        <div class="text-lg font-bold">{averageProgress.toFixed(0)}%</div>
    </Card>
</section>

<section class="relative grid md:grid-cols-2 lg:grid-cols-3 p-4">
    <Card>
        <div class="flex justify-between items-start w-full">
            <div class="flex-col items-center">
                <div class="flex items-center mb-1">
                    <h5 class="text-xl font-bold text-gray-900 dark:text-white me-1">Tasks Progress</h5>
                    <InfoCircleSolid id="donut1" class="w-3.5 h-3.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white cursor-pointer ms-1" />
                    <Popover triggeredBy="#donut1" class="text-sm text-gray-500 bg-white border border-gray-200 rounded-lg shadow-xs w-72 dark:bg-gray-800">
                    <div class="p-3 space-y-2">
                        <h3 class="font-semibold text-gray-900 dark:text-white">Tasks Progress</h3>
                        <p>This report shows the progress of tasks based on their priority.</p>
                    </div>
                    </Popover>
                </div>
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
        </div>
        
        <Chart {options} class="py-6" />
        
        <div class="grid grid-cols-1 border-gray-200 border-t dark:border-gray-700 justify-between">
            <div class="flex justify-between items-center pt-5">
            <Button class="text-sm font-medium hover:text-gray-900 dark:hover:text-white">
                {selectedPeriod} <ChevronDownOutline class="w-2.5 ms-1.5" />
            </Button>
            <Dropdown>
                <DropdownItem on:click={() => selectPeriod('Today')}>Today</DropdownItem>
                <DropdownItem on:click={() => selectPeriod('Last 7 days')}>Last 7 days</DropdownItem>
                <DropdownItem on:click={() => selectPeriod('Last 30 days')}>Last 30 days</DropdownItem>
            </Dropdown>                    
            <a href="/progress-report" class="uppercase text-sm font-semibold hover:text-primary-700 dark:hover:text-primary-500 px-3 py-2">
                PROGRESS REPORT <ChevronRightOutline class="w-5 h-5 ms-1 inline" />
            </a>
            </div>
        </div>
    </Card>
    
    <Card>
        <div class="flex justify-between items-start w-full">
            <div class="flex-col items-center">
                <div class="flex items-center mb-1">
                    <h5 class="text-xl font-bold text-gray-900 dark:text-white me-1">Progress Trend</h5>
                    <InfoCircleSolid id="donut2" class="w-3.5 h-3.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white cursor-pointer ms-1" />
                    <Popover triggeredBy="#donut2" class="text-sm text-gray-500 bg-white border border-gray-200 rounded-lg shadow-xs w-72 dark:bg-gray-800">
                    <div class="p-3 space-y-2">
                        <h3 class="font-semibold text-gray-900 dark:text-white">Progress Trend</h3>
                        <p>This report shows the progress trend over the selected period.</p>
                    </div>
                    </Popover>
                </div>
            </div>
        </div>
        <div class="mt-6 p-4 bg-gray-800 rounded-xl text-white shadow">
          <div class="text-md font-semibold mb-2">📈 Progress Trend (Last 7 days)</div>
          {#if trendOptions}
            <Chart options={trendOptions} class="h-64" />
          {:else}
            <p>Loading chart...</p>
          {/if}
        </div>
    </Card>
    
    <Card>
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center w-full gap-2">
          <div class="flex-col">
            <div class="flex items-center mb-1">
              <h5 class="text-xl font-bold text-gray-900 dark:text-white me-1">Latest Tasks</h5>
              <InfoCircleSolid
                id="donut3"
                class="w-4 h-4 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white cursor-pointer ms-1"
              />
              <Popover triggeredBy="#donut3" class="text-sm text-gray-500 bg-white border border-gray-200 rounded-lg shadow-xs w-72 dark:bg-gray-800">
                <div class="p-3 space-y-2">
                  <h3 class="font-semibold text-gray-900 dark:text-white">Latest Tasks</h3>
                  <p>This report shows the latest tasks created or updated.</p>
                </div>
              </Popover>
            </div>
          </div>
        </div>
      
        <div class="mt-6 p-4 bg-gray-800 rounded-xl text-white shadow space-y-3">
          <div class="text-md font-semibold flex items-center gap-2">
            📝 Latest Tasks
            <span class="text-xs font-normal text-gray-400">(Last updated just now)</span>
          </div>
          <ul class="space-y-1 text-sm text-gray-300">
            {#each latestTasks as task}
              <li class="hover:bg-gray-700 px-2 py-1 rounded-md transition flex justify-between items-center">
                <span>{task.title}</span>
                <span
                  class={`text-xs font-medium px-2 py-0.5 rounded-full
                    ${task.priority === 1 ? 'bg-red-500/20 text-red-400' :
                      task.priority === 2 ? 'bg-yellow-500/20 text-yellow-300' :
                      'bg-green-500/20 text-green-300'}`}
                >
                  {PRIORITY_MAP[task.priority]}
                </span>
              </li>
            {/each}
          </ul>
        </div>
    </Card>      
</section>
  
  