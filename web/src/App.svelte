<script lang="ts">
  import { post } from "./sdk";
  import { slide } from "svelte/transition";

  let inputCard = ""
  let inputName = ""

  let [error, loading, done, edit] = ["", false, false, false]

  function scan(uid: string) {
    loading = true
    post('/scan', { uid })
        .then(() => done = true)
        .catch(err => error = err)
        .finally(() => loading = false)
  }

  interface Card { id: string, name: string }

  let cards: Card[] = JSON.parse(localStorage.getItem("cards") || "[]")

  function addCard() {
    if (!inputCard || !inputName) return

    // Card must match either \d{20} or [0-9A-Fa-f]{16}
    if (!/^\d{20}$/.test(inputCard) && !/^[0-9A-Fa-f]{16}$/.test(inputCard))
      return error = "Invalid card ID"

    cards.push({ id: inputCard, name: inputName })
    cards = cards
    localStorage.setItem("cards", JSON.stringify(cards))
    inputCard = ""
    inputName = ""
  }

  function deleteCard(card: Card) {
    cards = cards.filter(c => c !== card)
    localStorage.setItem("cards", JSON.stringify(cards))
  }
</script>

<main>
  <h1>AimeWeb</h1>
  <p>点击一个卡就可以刷了，没有卡的话请先添加卡片。如果不知道卡号的话可以去 NFC Tools 扫</p>
  <div class="error">{error}</div>

  <div class="cards">
    {#each cards as card}
      <div class="flex gap-2">
        <button class="card" on:click={() => scan(card.id)}>{card.name} <span>{card.id}</span></button>
        {#if edit}
          <button transition:slide={{axis: "x"}}>删</button>
        {/if}
      </div>
    {/each}
  </div>

  <button on:click={() => edit = !edit}>编辑</button>

  <h2>添加卡片</h2>

  <div class="controls">
    <div class="input">
      <label for="add-card">卡号</label>
      <input id="add-card" placeholder="卡号 (e.g. 50001234123412341234)" bind:value={inputCard}>
    </div>
    <div class="input">
      <label for="add-name">名称</label>
      <input id="add-name" placeholder="名称 (e.g. Aime)" bind:value={inputName}>
    </div>
    <button on:click={addCard}>添加</button>
  </div>
</main>

<style lang="sass">
main
  display: flex
  flex-direction: column
  gap: 10px
  max-width: 500px
  margin: 0 auto

  > h1
    font-size: 2rem
    margin: 0

  > h2
    font-size: 1.5rem
    margin: 50px 0 0

  .error
    color: #ff6e6e

  .flex-h
    display: flex
    align-items: center
    justify-content: center
    width: 100%
    gap: 10px

  .card
    text-align: left
    display: flex
    justify-content: space-between
    padding: 1rem
    width: 100%

    span
      opacity: 0.8

  .controls
    display: flex
    flex-direction: column
    gap: 10px

  .input
    display: flex
    flex-direction: column
    align-items: flex-start
    width: 100%
    gap: 5px

  input, textarea
    border-radius: 8px
    border: 1px solid transparent
    padding: 0.6em 1.2em
    font-size: 1em
    font-weight: 500
    font-family: inherit
    background-color: rgba(0, 0, 0, 0.2)
    transition: all 0.5s ease
    box-sizing: border-box
    resize: none
    width: 100%

  input:focus, input:focus-visible
    border: 1px solid #646cff
    outline: none

  //input.warning
  //  border: 1px solid vars.$c-warning
  //
  //input.error
  //  border: 1px solid vars.$c-error
</style>
