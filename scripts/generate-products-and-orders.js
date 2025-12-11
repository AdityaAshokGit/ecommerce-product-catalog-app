const fs = require("fs");
const path = require("path");

// Product templates with real Unsplash images
const productTemplates = {
  Electronics: [
    {
      name: "Wireless Headphones",
      brands: ["Sony", "Bose", "Sennheiser", "Audio-Technica"],
      priceRange: [150, 400],
      image:
        "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400",
      tags: ["wireless", "audio", "bluetooth"],
    },
    {
      name: "Smartphone",
      brands: ["Apple", "Samsung", "Google", "OnePlus"],
      priceRange: [699, 1299],
      image:
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
      tags: ["smartphone", "5g", "mobile"],
    },
    {
      name: "Laptop",
      brands: ["Apple", "Dell", "HP", "Lenovo"],
      priceRange: [899, 2499],
      image:
        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400",
      tags: ["laptop", "computer", "productivity"],
    },
    {
      name: "Tablet",
      brands: ["Apple", "Samsung", "Microsoft", "Amazon"],
      priceRange: [299, 1099],
      image: "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
      tags: ["tablet", "portable", "touchscreen"],
    },
    {
      name: "Smartwatch",
      brands: ["Apple", "Samsung", "Garmin", "Fitbit"],
      priceRange: [199, 799],
      image:
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
      tags: ["smartwatch", "fitness", "wearable"],
    },
    {
      name: "Bluetooth Speaker",
      brands: ["JBL", "Bose", "Sony", "Ultimate Ears"],
      priceRange: [49, 299],
      image:
        "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
      tags: ["speaker", "bluetooth", "portable"],
    },
    {
      name: "Wireless Earbuds",
      brands: ["Apple", "Samsung", "Sony", "Jabra"],
      priceRange: [99, 299],
      image:
        "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=400",
      tags: ["earbuds", "wireless", "audio"],
    },
    {
      name: "Gaming Console",
      brands: ["Sony", "Microsoft", "Nintendo"],
      priceRange: [299, 499],
      image:
        "https://images.unsplash.com/photo-1486401899868-0e435ed85128?w=400",
      tags: ["gaming", "console", "entertainment"],
    },
    {
      name: "Camera",
      brands: ["Canon", "Nikon", "Sony", "Fujifilm"],
      priceRange: [599, 2999],
      image:
        "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400",
      tags: ["camera", "photography", "professional"],
    },
    {
      name: "Monitor",
      brands: ["Dell", "LG", "Samsung", "BenQ"],
      priceRange: [199, 899],
      image:
        "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400",
      tags: ["monitor", "display", "productivity"],
    },
    {
      name: "Keyboard",
      brands: ["Logitech", "Razer", "Corsair", "Keychron"],
      priceRange: [49, 199],
      image:
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400",
      tags: ["keyboard", "mechanical", "gaming"],
    },
    {
      name: "Mouse",
      brands: ["Logitech", "Razer", "SteelSeries"],
      priceRange: [29, 149],
      image:
        "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
      tags: ["mouse", "gaming", "wireless"],
    },
    {
      name: "Router",
      brands: ["TP-Link", "Netgear", "Asus", "Linksys"],
      priceRange: [79, 399],
      image:
        "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=400",
      tags: ["router", "wifi", "networking"],
    },
    {
      name: "External SSD",
      brands: ["Samsung", "SanDisk", "WD", "Crucial"],
      priceRange: [89, 299],
      image:
        "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400",
      tags: ["storage", "ssd", "portable"],
    },
    {
      name: "Webcam",
      brands: ["Logitech", "Razer", "Microsoft"],
      priceRange: [69, 199],
      image:
        "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400",
      tags: ["webcam", "video", "streaming"],
    },
  ],
  Clothing: [
    {
      name: "T-Shirt",
      brands: ["Nike", "Adidas", "Patagonia", "Uniqlo"],
      priceRange: [19, 49],
      image:
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
      tags: ["casual", "cotton", "everyday"],
    },
    {
      name: "Jeans",
      brands: ["Levi's", "Wrangler", "Lee", "AG"],
      priceRange: [59, 149],
      image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
      tags: ["denim", "jeans", "casual"],
    },
    {
      name: "Sneakers",
      brands: ["Nike", "Adidas", "New Balance", "Vans"],
      priceRange: [69, 179],
      image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
      tags: ["shoes", "sneakers", "athletic"],
    },
    {
      name: "Running Shoes",
      brands: ["Nike", "Brooks", "Asics", "Hoka"],
      priceRange: [89, 189],
      image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
      tags: ["running", "athletic", "performance"],
    },
    {
      name: "Hoodie",
      brands: ["Nike", "Champion", "Carhartt", "Patagonia"],
      priceRange: [49, 129],
      image: "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400",
      tags: ["hoodie", "casual", "comfortable"],
    },
    {
      name: "Jacket",
      brands: ["The North Face", "Patagonia", "Columbia", "Arc'teryx"],
      priceRange: [99, 399],
      image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
      tags: ["jacket", "outdoor", "weather-resistant"],
    },
    {
      name: "Dress Shirt",
      brands: ["Brooks Brothers", "Ralph Lauren", "Calvin Klein"],
      priceRange: [59, 149],
      image:
        "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=400",
      tags: ["formal", "dress-shirt", "professional"],
    },
    {
      name: "Backpack",
      brands: ["Herschel", "The North Face", "Patagonia", "Fjällräven"],
      priceRange: [49, 159],
      image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
      tags: ["backpack", "bag", "travel"],
    },
    {
      name: "Baseball Cap",
      brands: ["New Era", "Nike", "Carhartt"],
      priceRange: [24, 49],
      image:
        "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400",
      tags: ["hat", "cap", "accessory"],
    },
    {
      name: "Socks",
      brands: ["Bombas", "Smartwool", "Darn Tough"],
      priceRange: [14, 29],
      image:
        "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=400",
      tags: ["socks", "comfort", "everyday"],
    },
    {
      name: "Yoga Pants",
      brands: ["Lululemon", "Athleta", "Nike", "Alo"],
      priceRange: [69, 128],
      image:
        "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400",
      tags: ["activewear", "yoga", "athletic"],
    },
    {
      name: "Winter Coat",
      brands: ["Canada Goose", "Moncler", "The North Face"],
      priceRange: [299, 999],
      image:
        "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400",
      tags: ["coat", "winter", "warm"],
    },
    {
      name: "Shorts",
      brands: ["Nike", "Patagonia", "Lululemon"],
      priceRange: [39, 79],
      image:
        "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400",
      tags: ["shorts", "summer", "casual"],
    },
    {
      name: "Dress",
      brands: ["Zara", "H&M", "Reformation"],
      priceRange: [59, 199],
      image:
        "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",
      tags: ["dress", "formal", "fashion"],
    },
    {
      name: "Suit",
      brands: ["Hugo Boss", "Brooks Brothers", "Suit Supply"],
      priceRange: [399, 1299],
      image:
        "https://images.unsplash.com/photo-1594938291221-94f18cbb5660?w=400",
      tags: ["suit", "formal", "professional"],
    },
  ],
  "Home & Garden": [
    {
      name: "Coffee Maker",
      brands: ["Keurig", "Nespresso", "Breville", "Cuisinart"],
      priceRange: [79, 599],
      image:
        "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400",
      tags: ["coffee", "kitchen", "appliance"],
    },
    {
      name: "Vacuum Cleaner",
      brands: ["Dyson", "Shark", "iRobot", "Bissell"],
      priceRange: [199, 699],
      image: "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400",
      tags: ["vacuum", "cleaning", "home"],
    },
    {
      name: "Air Purifier",
      brands: ["Dyson", "Coway", "Levoit", "Honeywell"],
      priceRange: [149, 549],
      image:
        "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",
      tags: ["air-purifier", "health", "home"],
    },
    {
      name: "Desk Lamp",
      brands: ["BenQ", "TaoTronics", "Philips"],
      priceRange: [39, 149],
      image:
        "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400",
      tags: ["lamp", "lighting", "desk"],
    },
    {
      name: "Desk Chair",
      brands: ["Herman Miller", "Steelcase", "Secretlab"],
      priceRange: [299, 1299],
      image:
        "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400",
      tags: ["chair", "office", "ergonomic"],
    },
    {
      name: "Desk",
      brands: ["IKEA", "Uplift", "Autonomous"],
      priceRange: [199, 899],
      image:
        "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=400",
      tags: ["desk", "office", "furniture"],
    },
    {
      name: "Blender",
      brands: ["Vitamix", "Ninja", "Blendtec"],
      priceRange: [59, 449],
      image:
        "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400",
      tags: ["blender", "kitchen", "appliance"],
    },
    {
      name: "Air Fryer",
      brands: ["Ninja", "Philips", "Cosori"],
      priceRange: [89, 249],
      image:
        "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400",
      tags: ["air-fryer", "cooking", "kitchen"],
    },
    {
      name: "Bedding Set",
      brands: ["Brooklinen", "Parachute", "Boll & Branch"],
      priceRange: [149, 449],
      image:
        "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400",
      tags: ["bedding", "sheets", "bedroom"],
    },
    {
      name: "Throw Pillow",
      brands: ["West Elm", "Pottery Barn", "CB2"],
      priceRange: [29, 79],
      image:
        "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400",
      tags: ["pillow", "decor", "home"],
    },
    {
      name: "Area Rug",
      brands: ["Ruggable", "West Elm", "Loloi"],
      priceRange: [149, 899],
      image:
        "https://images.unsplash.com/photo-1600166898405-da9535204843?w=400",
      tags: ["rug", "decor", "home"],
    },
    {
      name: "Smart Thermostat",
      brands: ["Nest", "Ecobee", "Honeywell"],
      priceRange: [129, 249],
      image: "https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=400",
      tags: ["smart-home", "thermostat", "energy"],
    },
    {
      name: "Cookware Set",
      brands: ["All-Clad", "Calphalon", "Cuisinart"],
      priceRange: [149, 699],
      image:
        "https://images.unsplash.com/photo-1584990347449-39b4aa32c4b7?w=400",
      tags: ["cookware", "kitchen", "pots-pans"],
    },
    {
      name: "Garden Tools Set",
      brands: ["Fiskars", "Corona", "Gardena"],
      priceRange: [49, 149],
      image:
        "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400",
      tags: ["garden", "tools", "outdoor"],
    },
    {
      name: "Indoor Plant",
      brands: ["The Sill", "Bloomscape", "Costa Farms"],
      priceRange: [19, 89],
      image:
        "https://images.unsplash.com/photo-1463320726281-696a485928c7?w=400",
      tags: ["plant", "indoor", "decor"],
    },
  ],
  "Sports & Outdoors": [
    {
      name: "Yoga Mat",
      brands: ["Manduka", "Lululemon", "Gaiam"],
      priceRange: [29, 129],
      image:
        "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400",
      tags: ["yoga", "fitness", "exercise"],
    },
    {
      name: "Dumbbells Set",
      brands: ["Bowflex", "CAP", "PowerBlock"],
      priceRange: [89, 399],
      image:
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400",
      tags: ["weights", "fitness", "strength"],
    },
    {
      name: "Resistance Bands",
      brands: ["TheraBand", "Fit Simplify", "Whatafit"],
      priceRange: [12, 39],
      image:
        "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400",
      tags: ["resistance", "fitness", "portable"],
    },
    {
      name: "Camping Tent",
      brands: ["REI", "Coleman", "Big Agnes"],
      priceRange: [149, 549],
      image:
        "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400",
      tags: ["camping", "tent", "outdoor"],
    },
    {
      name: "Sleeping Bag",
      brands: ["The North Face", "Marmot", "REI"],
      priceRange: [89, 349],
      image:
        "https://images.unsplash.com/photo-1487730116645-74489c95b41b?w=400",
      tags: ["camping", "sleeping-bag", "outdoor"],
    },
    {
      name: "Hiking Boots",
      brands: ["Salomon", "Merrell", "Keen"],
      priceRange: [119, 249],
      image:
        "https://images.unsplash.com/photo-1520638023360-6e965ba4c0d0?w=400",
      tags: ["hiking", "boots", "outdoor"],
    },
    {
      name: "Water Bottle",
      brands: ["Hydroflask", "Yeti", "CamelBak"],
      priceRange: [24, 49],
      image:
        "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",
      tags: ["water-bottle", "hydration", "outdoor"],
    },
    {
      name: "Bicycle",
      brands: ["Trek", "Specialized", "Giant"],
      priceRange: [499, 2999],
      image:
        "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=400",
      tags: ["bicycle", "cycling", "outdoor"],
    },
    {
      name: "Bike Helmet",
      brands: ["Giro", "Bell", "POC"],
      priceRange: [49, 199],
      image:
        "https://images.unsplash.com/photo-1597318117760-0a5eecb07080?w=400",
      tags: ["helmet", "safety", "cycling"],
    },
    {
      name: "Kayak",
      brands: ["Perception", "Old Town", "Wilderness Systems"],
      priceRange: [499, 1499],
      image: "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400",
      tags: ["kayak", "water-sports", "outdoor"],
    },
    {
      name: "Fishing Rod",
      brands: ["Shimano", "Penn", "Ugly Stik"],
      priceRange: [39, 249],
      image: "https://images.unsplash.com/photo-1545450660-e3e2f6650b56?w=400",
      tags: ["fishing", "rod", "outdoor"],
    },
    {
      name: "Cooler",
      brands: ["Yeti", "Coleman", "Igloo"],
      priceRange: [49, 349],
      image:
        "https://images.unsplash.com/photo-1588200908342-23b585c03e26?w=400",
      tags: ["cooler", "camping", "outdoor"],
    },
    {
      name: "Paddleboard",
      brands: ["Bote", "iRocker", "Tower"],
      priceRange: [499, 1299],
      image:
        "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400",
      tags: ["paddleboard", "water-sports", "outdoor"],
    },
    {
      name: "Golf Clubs Set",
      brands: ["Callaway", "TaylorMade", "Titleist"],
      priceRange: [399, 1999],
      image:
        "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=400",
      tags: ["golf", "clubs", "sports"],
    },
    {
      name: "Tennis Racket",
      brands: ["Wilson", "Head", "Babolat"],
      priceRange: [79, 299],
      image:
        "https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=400",
      tags: ["tennis", "racket", "sports"],
    },
  ],
  Books: [
    {
      name: "Atomic Habits",
      brands: ["Clear"],
      priceRange: [16, 28],
      image: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
      tags: ["self-help", "productivity", "habits"],
    },
    {
      name: "The Psychology of Money",
      brands: ["Housel"],
      priceRange: [14, 26],
      image:
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400",
      tags: ["finance", "psychology", "money"],
    },
    {
      name: "Educated",
      brands: ["Westover"],
      priceRange: [15, 28],
      image:
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",
      tags: ["memoir", "biography", "education"],
    },
    {
      name: "Project Hail Mary",
      brands: ["Weir"],
      priceRange: [16, 29],
      image:
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
      tags: ["sci-fi", "fiction", "space"],
    },
    {
      name: "The Lean Startup",
      brands: ["Ries"],
      priceRange: [15, 27],
      image: "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400",
      tags: ["business", "startup", "entrepreneurship"],
    },
    {
      name: "Sapiens",
      brands: ["Harari"],
      priceRange: [17, 30],
      image:
        "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400",
      tags: ["history", "anthropology", "non-fiction"],
    },
    {
      name: "The Midnight Library",
      brands: ["Haig"],
      priceRange: [14, 27],
      image:
        "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400",
      tags: ["fiction", "contemporary", "fantasy"],
    },
    {
      name: "Thinking Fast and Slow",
      brands: ["Kahneman"],
      priceRange: [16, 30],
      image:
        "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=400",
      tags: ["psychology", "behavioral-economics", "science"],
    },
    {
      name: "Where the Crawdads Sing",
      brands: ["Owens"],
      priceRange: [15, 28],
      image:
        "https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=400",
      tags: ["fiction", "mystery", "bestseller"],
    },
    {
      name: "The Subtle Art of Not Giving a F*ck",
      brands: ["Manson"],
      priceRange: [13, 25],
      image:
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",
      tags: ["self-help", "philosophy", "life-advice"],
    },
    {
      name: "Dune",
      brands: ["Herbert"],
      priceRange: [16, 29],
      image:
        "https://images.unsplash.com/photo-1580537659466-0a9bfa916a54?w=400",
      tags: ["sci-fi", "classic", "fiction"],
    },
    {
      name: "The Four Agreements",
      brands: ["Ruiz"],
      priceRange: [12, 22],
      image:
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",
      tags: ["self-help", "spirituality", "wisdom"],
    },
    {
      name: "Deep Work",
      brands: ["Newport"],
      priceRange: [15, 27],
      image: "https://images.unsplash.com/photo-1518171539-a8c4e951feb4?w=400",
      tags: ["productivity", "focus", "business"],
    },
    {
      name: "The Alchemist",
      brands: ["Coelho"],
      priceRange: [13, 24],
      image: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
      tags: ["fiction", "philosophy", "adventure"],
    },
    {
      name: "1984",
      brands: ["Orwell"],
      priceRange: [12, 22],
      image: "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400",
      tags: ["classic", "dystopian", "fiction"],
    },
  ],
};

// Helper functions
function randomFromArray(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomPrice(min, max) {
  return Number((Math.random() * (max - min) + min).toFixed(2));
}

function randomRating() {
  return Number((Math.random() * 2 + 3).toFixed(1)); // 3.0 to 5.0
}

function generateProducts(count = 2000) {
  const products = [];
  let productId = 1;

  const categories = Object.keys(productTemplates);

  // Generate products by cycling through templates
  while (products.length < count) {
    for (const category of categories) {
      const templates = productTemplates[category];

      for (const template of templates) {
        if (products.length >= count) break;

        // Generate 2-5 variants per template
        const variantCount = Math.floor(Math.random() * 4) + 2;

        for (let v = 0; v < variantCount; v++) {
          if (products.length >= count) break;

          const brand = randomFromArray(template.brands);
          const price = randomPrice(
            template.priceRange[0],
            template.priceRange[1]
          );
          const rating = randomRating();
          const inStock = Math.random() > 0.1; // 90% in stock

          const descriptors = [
            "Premium",
            "Professional",
            "Essential",
            "Classic",
            "Modern",
            "Advanced",
            "Compact",
            "Deluxe",
          ];
          const descriptor =
            Math.random() > 0.5 ? randomFromArray(descriptors) + " " : "";

          products.push({
            id: `PROD-${String(productId).padStart(4, "0")}`,
            name: `${brand} ${descriptor}${template.name}`,
            description: `High-quality ${template.name.toLowerCase()} from ${brand}. ${
              inStock ? "Available now" : "Coming soon"
            } with premium features and excellent reviews.`,
            price,
            category,
            brand,
            rating,
            inStock,
            imageUrl: template.image,
            tags: template.tags,
          });

          productId++;
        }
      }
    }
  }

  return products.slice(0, count);
}

function generateOrders(products, count = 5000) {
  const orders = [];
  const customerIds = Array.from(
    { length: 800 },
    (_, i) => `CUST-${String(i + 1).padStart(4, "0")}`
  );

  // Create a weighted product list (some products are more popular)
  const popularProducts = [];
  products.forEach((product) => {
    // More expensive items are less likely to be purchased
    const weight = product.price < 100 ? 5 : product.price < 300 ? 3 : 1;
    for (let i = 0; i < weight; i++) {
      popularProducts.push(product);
    }
  });

  // Generate orders over the past 12 months
  const now = new Date();
  const oneYearAgo = new Date(
    now.getFullYear() - 1,
    now.getMonth(),
    now.getDate()
  );

  for (let i = 0; i < count; i++) {
    // Random date in the past year
    const orderDate = new Date(
      oneYearAgo.getTime() +
        Math.random() * (now.getTime() - oneYearAgo.getTime())
    );

    // Random customer (some customers order more frequently)
    const customerId = randomFromArray(customerIds);

    // 1-4 items per order
    const itemCount = Math.floor(Math.random() * 4) + 1;
    const orderItems = [];
    const selectedProducts = new Set();

    for (let j = 0; j < itemCount; j++) {
      let product = randomFromArray(popularProducts);

      // Avoid duplicate products in same order
      let attempts = 0;
      while (selectedProducts.has(product.id) && attempts < 10) {
        product = randomFromArray(popularProducts);
        attempts++;
      }

      selectedProducts.add(product.id);

      // Quantity (1-3, weighted towards 1)
      const quantity = Math.random() < 0.7 ? 1 : Math.random() < 0.8 ? 2 : 3;

      orderItems.push({
        productId: product.id,
        quantity,
        price: product.price,
      });
    }

    const total = orderItems.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );

    orders.push({
      orderId: `ORD-${String(i + 1).padStart(5, "0")}`,
      date: orderDate.toISOString(),
      customerId,
      items: orderItems,
      total: Number(total.toFixed(2)),
    });
  }

  // Sort by date
  orders.sort((a, b) => new Date(a.date) - new Date(b.date));

  return orders;
}

// Generate and save data
console.log("Generating products...");
const products = generateProducts(2000);
console.log(`✓ Generated ${products.length} products`);

console.log("Generating orders...");
const orders = generateOrders(products, 5000);
console.log(`✓ Generated ${orders.length} orders`);

// Save to files
const dataDir = path.join(__dirname, "../data");

// Create data directory if it doesn't exist
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
  console.log("✓ Created data directory");
}

fs.writeFileSync(
  path.join(dataDir, "products.json"),
  JSON.stringify(products, null, 2)
);
console.log("✓ Saved products.json");

fs.writeFileSync(
  path.join(dataDir, "orders.json"),
  JSON.stringify(orders, null, 2)
);
console.log("✓ Saved orders.json");

// Generate some statistics
const stats = {
  productCount: products.length,
  orderCount: orders.length,
  totalCustomers: new Set(orders.map((o) => o.customerId)).size,
  averageOrderValue: (
    orders.reduce((sum, o) => sum + o.total, 0) / orders.length
  ).toFixed(2),
  dateRange: {
    earliest: orders[0].date,
    latest: orders[orders.length - 1].date,
  },
  productsByCategory: {},
};

products.forEach((p) => {
  stats.productsByCategory[p.category] =
    (stats.productsByCategory[p.category] || 0) + 1;
});

console.log("\n📊 Dataset Statistics:");
console.log(JSON.stringify(stats, null, 2));

console.log("\n✅ Data generation complete!");
