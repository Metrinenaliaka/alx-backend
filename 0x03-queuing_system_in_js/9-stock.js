import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 5 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

function getItemById(id) {
  return listProducts.find(item => item.itemId === id);
}

function reserveStockById(itemId, stock) {
  const item = getItemById(itemId);
  client.set(item.itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  const item = getItemById(itemId);
  return await getAsync(item.itemId);
}

const client = redis.createClient();
client.on('error', (err) => console.error(err))
  .on('connect', () => console.log('Redis client connected'));

const getAsync = promisify(client.get).bind(client);

const app = express();
app.listen(1245);

app.get('/list_products', (req, res) => res.json(listProducts));
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);

  const item = getItemById(itemId);
  if (!item) res.json({ status: 'Product not found' });

  const stock = await getCurrentReservedStockById(itemId);
  if (stock === null) {
    reserveStockById(itemId, item.initialAvailableQuantity);
    item.currentQuantity = item.initialAvailableQuantity;
  }
  item.currentQuantity = stock;
  res.json(item);
});
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) res.json({ status: 'Product not found' });

  const currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock === null) {
    reserveStockById(itemId, item.initialAvailableQuantity - 1);
    res.json({ status: 'Reservation confirmed', itemId });
  }
  if (currentStock <= 0) {
    res.json({ status: 'Not enough stock available', itemId });
  } else {
    reserveStockById(itemId, currentStock - 1);
    res.json({ status: 'Reservation confirmed', itemId });
  }
});
