<script lang="ts">
  import { onMount } from "svelte";
  import { Button, Textarea } from "flowbite-svelte";
  import { getCommentsByTaskId, postComment } from "$lib/api/comments";
  import type { Comment } from "$lib/types/comment";
	import { MessagesSolid } from "flowbite-svelte-icons";

  export let taskId: string;

  let comments: Comment[] = [];
  let newComment = "";
  let isLoading = true;

  async function loadComments() {
    isLoading = true;
    try {
      comments = await getCommentsByTaskId(taskId);
    } catch (err) {
      console.error("Failed to load comments", err);
    } finally {
      isLoading = false;
    }
  }

  async function submitComment() {
    if (!newComment.trim()) return;
    const dummyAuthorId = Math.floor(Math.random() * 5) + 1;
    try {
      await postComment(taskId, newComment, dummyAuthorId);
      newComment = "";
      loadComments();
    } catch (err) {
      console.error("Failed to post comment", err);
    }
  }

  onMount(loadComments);
</script>

<div class="mt-10">
  <h2 class="text-xl font-bold mb-6 text-gray-900 dark:text-white"><MessagesSolid class="w-6 h-6 inline" /> Comments</h2>

  {#if isLoading}
    <p class="text-gray-500 dark:text-gray-400">Loading comments...</p>
  {:else if comments.length === 0}
    <p class="text-gray-500 dark:text-gray-400">No comments yet.</p>
  {:else}
    <ul class="space-y-2 mb-8">
      {#each comments as comment}
        <li class="flex gap-3 items-start py-4   shadow-md">
          <!-- Avatar / Initials -->
          <div class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold dark:bg-blue-500">
            {(comment.author.username || "A").charAt(0).toUpperCase()}
          </div>

          <!-- Comment Content -->
          <div class="bg-gray-100 dark:bg-gray-800 rounded-xl flex-1">
            <div class="flex justify-between items-center mb-1">
              <span class="font-semibold text-gray-900 dark:text-white">{comment.author.username || "Anonymous"}</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">{new Date(comment.created_at).toLocaleString()}</span>
            </div>
            <p class="text-gray-800 dark:text-gray-200 text-sm leading-relaxed whitespace-pre-wrap">{comment.content}</p>
          </div>
        </li>
      {/each}
    </ul>
  {/if}

  <!-- New Comment Box -->
  <div class="space-y-3">
    <Textarea
      bind:value={newComment}
      placeholder="Write a comment..."
      class="w-full min-h-[80px] bg-white dark:bg-gray-700 dark:text-white rounded-lg border border-gray-300 dark:border-gray-600 shadow-sm focus:ring-blue-500 focus:border-blue-500"
    />
    <div class="flex justify-end">
      <Button
        on:click={submitComment}
        class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg shadow px-5"
      >
        Post Comment
      </Button>
    </div>
  </div>
</div>
