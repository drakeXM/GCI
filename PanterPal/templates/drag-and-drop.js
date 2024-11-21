// Allow only one course per time slot
const weekdays = document.querySelectorAll('.week-day');

weekdays.forEach((weekday) => {
    const boxes = weekday.querySelectorAll('.time-slot'); // Select all the time slots under each day
    boxes.forEach((box) => {
        box.addEventListener('dragover', (event) => {
            event.preventDefault();  // Allow drop
        });

        box.addEventListener('drop', (event) => {
            event.preventDefault();

            const draggedCourse = document.querySelector('.dragging');
            if (draggedCourse) {
                // Check if there's already a course in the box
                if (box.querySelector('.course-box')) {
                    alert("This time slot is already filled. Please choose a different slot.");
                    return;
                }

                // If the box is empty, append the dragged course there
                box.appendChild(draggedCourse);
                draggedCourse.classList.remove('dragging');
                draggedCourse.setAttribute('draggable', false);  // Disable dragging for this course once dropped
            }
        });
    });
});

// Ensure that each course is draggable and can be moved around
const courseBoxes = document.querySelectorAll('.course-box');
courseBoxes.forEach((box) => {
    box.addEventListener('dragstart', (event) => {
        event.target.classList.add('dragging');
    });

    box.addEventListener('dragend', (event) => {
        event.target.classList.remove('dragging');
    });
});
