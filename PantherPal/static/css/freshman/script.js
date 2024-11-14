const courses = [
    { id: 1, name: "Introduction to Programming", time: "9:00 AM" },
    { id: 2, name: "Calculus I", time: "10:00 AM" },
    { id: 3, name: "Chemistry 101", time: "11:00 AM" },
    { id: 4, name: "Physics I", time: "1:00 PM" },
    { id: 5, name: "English Composition", time: "2:00 PM" },
    { id: 6, name: "History 101", time: "3:00 PM" }
  ];
  
  let selectedCourses = [];
  
  function searchCourses() {
    const searchInput = document.getElementById("course-search").value.toLowerCase();
    const filteredCourses = courses.filter(course => 
      course.name.toLowerCase().includes(searchInput)
    );
  
    const courseListDiv = document.getElementById("course-list");
    courseListDiv.innerHTML = "";
  
    filteredCourses.forEach(course => {
      const courseElement = document.createElement("div");
      courseElement.textContent = course.name;
      courseElement.classList.add("course-item");
      courseElement.setAttribute("draggable", "true");
      courseElement.setAttribute("data-id", course.id);
      courseElement.addEventListener("dragstart", dragStart);
      courseListDiv.appendChild(courseElement);
    });
  }
  
  function dragStart(e) {
    e.dataTransfer.setData("courseId", e.target.getAttribute("data-id"));
  }
  
  const timeSlots = document.querySelectorAll(".time-slot");
  
  timeSlots.forEach(slot => {
    slot.addEventListener("dragover", dragOver);
    slot.addEventListener("drop", dropCourse);
  });
  
  function dragOver(e) {
    e.preventDefault();
  }
  
  function dropCourse(e) {
    e.preventDefault();
  
    const courseId = e.dataTransfer.getData("courseId");
    const course = courses.find(c => c.id == courseId);
    const timeSlot = e.target;
  
    if (!timeSlot.querySelector(".course-in-schedule")) {
      const courseDiv = document.createElement("div");
      courseDiv.classList.add("course-in-schedule");
      courseDiv.textContent = course.name;
      timeSlot.appendChild(courseDiv);
    }
  }
  
  // Initialize the course search and setup
  searchCourses();
  