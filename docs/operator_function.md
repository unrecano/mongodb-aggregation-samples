# Operator Function

```javascript
[
  {
    $addFields: {
      wordCount: {
        $function: {
          body: function (description) {
            if (description) {
              var words = description.split(" ");
              return words.length;
            } else {
              return 0;
            }
          },
          args: ["$description"],
          lang: "js"
        }
      }
    }
  },
  {
    $group: {
      _id: "$property_type",
      averageWordCount: {
        $avg: "$wordCount"
      }
    }
  },
  {
    $sort: {
      averageWordCount: -1
    }
  }
]
```