let totalCaloriesBurned = 0;
let totalCaloriesConsumed = 0;

document.getElementById("exercise-form").addEventListener("submit", function(e) {
    e.preventDefault();
    
    const exerciseType = document.getElementById("exercise-type").value;
    const duration = parseInt(document.getElementById("exercise-duration").value);
    
    // 運動ごとの消費カロリー (仮の値: 1分あたり)
    const calorieRates = {
        "ランニング": 10,
        "ウォーキング": 5,
        "サイクリング": 8
    };
    
    const caloriesBurned = duration * calorieRates[exerciseType];
    totalCaloriesBurned += caloriesBurned;
    
    document.getElementById("exercise-results").innerHTML += 
        `<p>${exerciseType}を${duration}分行いました: ${caloriesBurned} kcal消費</p>`;
    
    updateCalories();
});

document.getElementById("meal-form").addEventListener("submit", function(e) {
    e.preventDefault();
    
    const mealName = document.getElementById("meal-name").value;
    const calories = parseInt(document.getElementById("calories").value);
    
    totalCaloriesConsumed += calories;
    
    document.getElementById("meal-results").innerHTML += 
        `<p>${mealName}: ${calories} kcal摂取</p>`;
    
    updateCalories();
});

function updateCalories() {
    document.getElementById("total-calories").textContent = `消費カロリー: ${totalCaloriesBurned} kcal`;
    document.getElementById("total-consumed").textContent = `摂取カロリー: ${totalCaloriesConsumed} kcal`;
}
