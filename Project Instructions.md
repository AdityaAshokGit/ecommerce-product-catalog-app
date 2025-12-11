# Take-Home Assignment - E-commerce Product Search & Filter

## Overview

Build a product catalog application with search and filtering capabilities. You'll be working with a dataset of products and order history to create both backend API endpoints and a frontend interface to browse, search, and filter products.

**Time Expectation:** 4-6 hours

## What We're Looking For

We want to see how you:

- Structure and organize code
- Make architectural decisions appropriate to the problem
- Handle edge cases and errors
- Write clean, maintainable code
- Prioritize features and manage scope

## AI Usage

Feel free to use AI - in fact, we encourage it. Be prepared to talk through your code and reasoning during the live demo.

**Important:** Focus on demonstrating strong fundamentals and good engineering judgment. We value quality over quantity.

## Core Requirements

Build a product catalog that allows users to:

1. **Product Display**

   - View a list of products with basic information (name, price, category, image, rating)
   - Display products in a clean, responsive grid layout

2. **Search Functionality**

   - Search products by name or description
   - Display search results dynamically

3. **Filtering**

   - Filter by category
   - Filter by price range (min/max)
   - Filter by brand
   - Apply multiple filters simultaneously

4. **Sorting**

   - Sort by price (low to high, high to low)
   - Sort by rating
   - Sort by most popular (based on order history)

5. **Most Popular Filter**

   - Use the provided `orders.json` file to calculate product popularity
   - Implement a "Most Popular" sort option that ranks products by purchase count
   - Display a purchase count or popularity indicator on product cards

6. **User Experience**

   - Loading states during data fetching
   - Empty states when no products match filters
   - Error handling with user-friendly messages
   - Clear visual feedback for applied filters

7. **Testing**
   - Unit tests for critical business logic
   - (Optional) Integration tests for API endpoints
   - (Optional) Frontend component tests

## Bonus Features (Optional)

These are not required but feel free to do them if you would like to demonstrate additional technical depth.

1. \*_Frequently Co-Purchased Recommendations_

   - Implement an API endpoint that returns products frequently bought together
   - Use order history to identify co-purchase patterns
   - Display recommendations on product detail view or as a separate section

2. **Advanced Filtering**

   - Faceted search with result counts per filter option
   - Filter by availability (in stock/out of stock)
   - Tag-based filtering

3. **Performance Optimizations**

   - Pagination or infinite scroll
   - Debounced search input
   - Caching strategies

4. **URL State Management**
   - Persist filters and search in URL query parameters
   - Shareable URLs with applied filters

## Technical Stack

Feel free to build this in the language and stack of your choice. We have provided 2 sample data files - you are welcome to build on top of these.

- **Data**:
  - `sample-products.json` - small sample file with products data
  - `sample-orders.json` - small sample file with order data

We have also included `scripts/generate-products-and-orders.js` which you can run to generate much larger product and order datasets to test and demo with.

Feel free to modify the scaffolding or use different tools if you prefer, but be prepared to explain your choices.

## Dataset Details

### Products (`products.json`)

Each product has:

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price": number,
  "category": "string",
  "brand": "string",
  "rating": number,
  "inStock": boolean,
  "imageUrl": "string",
  "tags": ["string"]
}
```

### Orders (`orders.json`)

Each order contains:

```json
{
  "orderId": "string",
  "date": "ISO date string",
  "customerId": "string",
  "items": [
    {
      "productId": "string",
      "quantity": number,
      "price": number
    }
  ],
  "total": number
}
```

## Deliverables

1. **Working Code**: Your implementation should run locally with clear setup instructions
2. **README**: Include:
   - Setup and running instructions
   - Overview of your approach and architecture
   - Explanation of how you calculated popularity and (if applicable) co-purchase recommendations
   - Any assumptions or tradeoffs you made
   - What you would do with more time
   - Which bonus features you implemented (if any)
   - Known limitations or bugs
3. **Tests** (if included): Instructions on how to run them

## Live Discussion

After you submit, we'll schedule a 45-60 minute session where you'll:

- Walk us through your code and architectural decisions
- Run the application and demonstrate key features
- Explain your popularity calculation approach
- Discuss tradeoffs and alternative approaches
- Potentially pair on extending a feature or fixing a bug

## Evaluation Criteria

We'll be looking at:

- **Code Quality**: Readability, organization, and maintainability
- **Functionality**: Does it work? Does it handle edge cases?
- **Architecture**: Are the abstractions appropriate? Is it extensible?
- **User Experience**: Is the interface intuitive and responsive? You can use very basic designs - we will not be judging that.
- **Problem Solving**: How did you approach the popularity/co-purchase calculations?
- **Communication**: Can you clearly explain your decisions?
- **Pragmatism**: Did you scope appropriately and prioritize well?

**Note**: Completing bonus features is not required to be successful. We'd rather see excellent execution on core requirements than rushed implementations of everything.

## Getting Started

1. Clone the repository (or download the scaffolding)
2. Follow the setup instructions in the scaffolding README
3. Start with the core requirements
4. Add bonus features based on time and interest
5. Document your work as you go

## Questions?

If you have any questions about the requirements or run into technical issues with the scaffolding, please reach out to our Talent team. We're happy to clarify!

## Submission

Please submit your solution as:

- A GitHub repository (preferred)
  Include a README with setup instructions and your approach overview.

**Good luck! We're excited to see what you build.**
