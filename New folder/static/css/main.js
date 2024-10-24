// Function to update the progress circle
function updateProgress(percentage) {
    const progressCircle = document.querySelector('.progress-bar');
    const textElement = document.getElementById('progress-text');
    
    // Total length of the circle's stroke
    const radius = 45;
    const circumference = 2 * Math.PI * radius;
    
    // Set the stroke-dasharray and stroke-dashoffset based on the percentage
    progressCircle.style.strokeDasharray = `${circumference}`;
    progressCircle.style.strokeDashoffset = `${circumference - (percentage / 100) * circumference}`;
    
    // Update the percentage text inside the circle
    textElement.textContent = `${percentage}%`;
}

// Call this function with the student's completion percentage
updateProgress(75);  // Example: 75% complete

// Function to redirect to the courses page when the circle is clicked
function goToCourses() {
    window.location.href = "/courses";
}
