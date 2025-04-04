<script lang="ts">
    import { onMount } from "svelte";
    import { Input, Button, Textarea } from "flowbite-svelte";
    import { getCommentsByTaskId, postComment } from "$lib/api/comments";
    import type { Comment } from "$lib/types/comment";
  
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
      try {
        await postComment(taskId, newComment);
        newComment = "";
        loadComments();
      } catch (err) {
        console.error("Failed to post comment", err);
      }
    }
  
    onMount(loadComments);
  </script>
  
  <div class="mt-8">
    <h2 class="text-lg font-semibold mb-4 text-gray-800 dark:text-white">Comments</h2>
  
    {#if isLoading}
      <p class="text-gray-500">Loading comments...</p>
    {:else if comments.length === 0}
      <p class="text-gray-500">No comments yet.</p>
    {:else}
      <ul class="space-y-4 mb-6">
        {#each comments as comment}
          <li class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg shadow-sm">
            <p class="text-gray-900 dark:text-white">{comment.content}</p>
            <small class="text-sm text-gray-500">{comment.author || "Anonymous"} • {new Date(comment.created_at).toLocaleString()}</small>
          </li>
        {/each}
      </ul>
    {/if}
  
    <div class="space-y-2">
      <Textarea bind:value={newComment} placeholder="Write a comment..." class="dark:bg-gray-700 dark:text-white" />
      <Button on:click={submitComment} class="bg-blue-600 hover:bg-blue-700 text-white">Post Comment</Button>
    </div>
  </div>
  