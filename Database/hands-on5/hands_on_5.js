// =========================
// TASK 1
// =========================

// Question 64
db.feedback.countDocuments()

// =========================
// TASK 2
// =========================

// Question 65
db.feedback.find({ rating: 5 })

// Question 66
db.feedback.find({
    course_code: "CS101",
    tags: "challenging"
})

// Question 67
db.feedback.find(
{},
{
    student_id:1,
    course_code:1,
    rating:1,
    _id:0
}
)

// Question 68
db.feedback.updateMany(
{
    rating:{$lt:3}
},
{
    $set:{
        needs_review:true
    }
})

db.feedback.find({
needs_review:true
})

// Question 69
db.feedback.updateMany(
{
needs_review:true
},
{
$push:{
tags:"reviewed"
}
})

db.feedback.find({
needs_review:true
})

// Question 70
db.feedback.deleteMany({
semester:"2021-EVEN"
})

db.feedback.find({
semester:"2021-EVEN"
})

// =========================
// TASK 3
// =========================

// Question 71
db.feedback.aggregate([
{
$match:{
semester:"2022-ODD"
}
},
{
$group:{
_id:"$course_code",
avg_rating:{
$avg:"$rating"
},
feedback_count:{
$sum:1
}
}
},
{
$sort:{
avg_rating:-1
}
}
])

// Question 72
db.feedback.aggregate([
{
$match:{
semester:"2022-ODD"
}
},
{
$group:{
_id:"$course_code",
avg_rating:{
$avg:"$rating"
},
feedback_count:{
$sum:1
}
}
},
{
$project:{
_id:0,
course_code:"$_id",
average_rating:{
$round:[
"$avg_rating",
1
]
},
feedback_count:1
}
},
{
$sort:{
average_rating:-1
}
}
])

// Question 73
db.feedback.aggregate([
{
$unwind:"$tags"
},
{
$group:{
_id:"$tags",
count:{
$sum:1
}
}
},
{
$sort:{
count:-1
}
}
])

// Question 74
db.feedback.createIndex({
course_code:1
})

db.feedback.find({
course_code:"CS101"
}).explain("executionStats")