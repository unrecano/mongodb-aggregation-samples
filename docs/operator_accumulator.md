# Operator Accumulator

```javascript
[
  {
    $match: {
      "review_scores.review_scores_rating": {
        $gt: 90
      }
    }
  },
  {
    $addFields: {
      amenitiesSize: { $size: "$amenities" }
    }
  },
  {
    $group: {
      _id: null,
      media: {
        $accumulator: {
          init: function () {
            return { sum: 0, count: 0 };
          },
          accumulateArgs: ["$amenitiesSize"],
          accumulate: function (state, size) {
            return {
              sum: state.sum + size,
              count: state.count + 1
            };
          },
          merge: function (before, current) {
            return {
              sum: before.sum + current.sum,
              count: before.count + current.count
            };
          },
          finalize: function (state) {
            return state.count > 0 ? state.sum / state.count : 0;
          },
          lang: "js"
        }
      }
    }
  }
]
```