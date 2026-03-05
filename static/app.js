const grid = document.getElementById('item-grid');

// fetch all items and render cards
async function loadItems() {
  const res = await fetch('/api/items');
  const items = await res.json();
  grid.innerHTML = '';
  items.forEach(item => grid.appendChild(createCard(item)));
}

// build a card element for one item
function createCard(item) {
  const card = document.createElement('div');
  card.className = 'card';
  card.id = `item-${item.id}`;
  if (item.count === 0) card.classList.add('empty');
  else if (item.is_low) card.classList.add('low');

  card.innerHTML = `
    <h2>${item.name}</h2>
    <div class="count">${item.count}</div>
    <div class="unit">${item.unit || ''}</div>
    <div class="buttons">
      <button onclick="adjust(${item.id}, -1)" ${item.count === 0 ? 'disabled' : ''}>−</button>
      <button onclick="adjust(${item.id}, +1)">+</button>
    </div>
  `;

  return card;
}

// send delta to flask, re-render that card
async function adjust(itemId, delta) {
  const res = await fetch(`/api/items/${itemId}/adjust`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ delta })
  });
  const updated = await res.json();

  // replace just the affected card
  const oldCard = document.getElementById(`item-${itemId}`);
  oldCard.replaceWith(createCard(updated));
}

loadItems();