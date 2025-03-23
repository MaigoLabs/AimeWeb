<script lang="ts">
  import { post } from "./sdk";

  let inputCard = ""
  let inputName = ""

  let [error, loading, done] = ["", false, false]

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
  <div class="error">{error}</div>

  {#each cards as card}
    <div class="card">
      <h2>{card.name}</h2>
      <p>{card.id}</p>
      <button on:click={() => scan(card.id)}>刷</button>
      <button on:click={() => deleteCard(card)}>删</button>
    </div>
  {/each}

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
