<script lang="ts">
  import Icon from "@iconify/svelte";
  import { post } from "./sdk";
  import { slide } from "svelte/transition";

  let inputCard = ""
  let inputName = ""

  let [error, loading, done, edit] = ["", false, false, false]

  function scan(uid: string) {
    if (loading) return
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
      return error = "卡号格式不对"

    // If already exist, remove existing
    cards = [...cards.filter(c => c.id !== inputCard), { id: inputCard, name: inputName }]
    localStorage.setItem("cards", JSON.stringify(cards))
    inputCard = ""
    inputName = ""
  }

  function deleteCard(card: Card) {
    cards = cards.filter(c => c !== card)
    localStorage.setItem("cards", JSON.stringify(cards))
  }
  
  const nfcAvail = 'NDEFReader' in window
  let nfcScanning = false

  async function startNFCScan() {
    if (!nfcAvail) return error = "NFC 不支持"

    if (nfcScanning) return
    nfcScanning = true

    try {
      const ndef = new NDEFReader()
      await ndef.scan()

      ndef.onreadingerror = () => { error = "读取 NFC 失败，试试别的卡" }
      ndef.onreading = ({message, serialNumber}: NDEFReadingEvent) => {
        console.log(serialNumber, message)
        
        const c = serialNumber?.toUpperCase().replaceAll(":", "")
        if (!c) return error = "无法读取卡号"
        
        if (c.startsWith("012E")) inputName = "FeliCa"
        else inputName = "NFC Card"
        
        // Force c to be 16-characters and starting with 012E
        inputCard = "012E" + c.padStart(16, "0").slice(4, 16)
      }
    } catch (err) { error = `无法启动 NFC，请检查权限或设备支持: ${err}` }
  }
</script>

<main>
  <h1>AimeWeb</h1>
  <p>点击一个卡就可以刷了，没有卡的话请先在下面添加卡片。
    {#if !nfcAvail} 如果不知道卡号的话可以用 NFC Tools App 扫 {/if}</p>
  <div class="error">{error}</div>

  <div class="cards flex flex-col gap-2">
    {#each cards as card}
      <div class="flex gap-2">
        <button class="card" on:click={() => scan(card.id)}>{card.name} <span>{card.id}</span></button>
        {#if edit}
          <button transition:slide={{axis: "x"}} on:click={() => deleteCard(card)}>删</button>
        {/if}
      </div>
    {/each}
  </div>

  <button on:click={() => edit = !edit}>编辑</button>

  <h2>添加卡片</h2>

  <div class="controls">
    <div class="input">
      <label for="add-card">卡号</label>
      <input id="add-card" placeholder="卡号 (e.g. 50001234123412341234)" bind:value={inputCard}
             on:keydown={(e: KeyboardEvent) => {
               // Ignore special keys
                if (e.key.length > 1) return

               // Prevent every key except 0-9 and A-F
                if (!/^[0-9A-Fa-f]$/.test(e.key)) e.preventDefault()
             }}>
    </div>
    <div class="input">
      <label for="add-name">名称</label>
      <input id="add-name" placeholder="名称 (e.g. Aime)" bind:value={inputName}>
    </div>
    <button on:click={addCard}>添加</button>
    {#if nfcAvail}
      <button on:click={startNFCScan}>
        {#if nfcScanning}
          <Icon icon="line-md:loading-twotone-loop" /> NFC 扫描中... 
        {:else}
          NFC 扫描
        {/if}
      </button>
    {/if}
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
