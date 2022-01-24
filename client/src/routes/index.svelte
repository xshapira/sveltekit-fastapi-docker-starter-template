<main>
  <form on:submit|preventDefault={handleSubmit}>
    <label for="frameworks">What is your favorite frontend framework?</label>
    <br>
    <select id="frameworks" bind:value={selectedFramework}>
      <option value="">-- Select one --</option>
      {#each frameworksList as framework}
        <option value={framework}>{framework}</option>
      {/each}
    </select>

    <br><br>

    <button type="submit">Submit Form</button>
    <button type="reset">Reset Form</button>
  </form>

  <br>

  <div>The server response: { serverResponse }</div>
</main>


<script>
  import { onMount } from "svelte";

  let frameworksList = [];
  let selectedFramework = "";
  let serverResponse = "";

  onMount(() => {
    getFrameworksList();
  });

  async function getFrameworksList() {
    try {
      const response = await fetch("/api/get-frameworks-list/");
      
      if (!response.ok) {
        throw Error(response.statusText);
      }

      frameworksList = await response.json();
    }
    catch(err) {
      console.error("getFrameworksList Error:", err);
    }
  }
  
  async function handleSubmit() {
    try {
      const response = await fetch("/api/submit-framework/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          selected_framework: selectedFramework
        }),
      });

      if (!response.ok) {
        throw Error(response.statusText);
      }
      
      let result = await response.json();
      serverResponse = result.message;
    }
    catch(err) {
      console.log("handleSubmit Error:", err);
    }
  }
</script>


<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  }
  
  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }

  select {
    width: 200px;
  }
</style>
