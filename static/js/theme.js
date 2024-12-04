console.log("theme.js is loaded and running!");

/**
 * Bubbly - Bootstrap 5 Dashboard & CMS Theme v. 1.3.2
 * Homepage:
 * Copyright 2023, Bootstrapious - https://bootstrapious.com
 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {
    // ------------------------------------------------------- //
    // Sidebar
    // ------------------------------------------------------ //

    const sidebarToggler = document.querySelector(".sidebar-toggler");

    if (sidebarToggler) {
        sidebarToggler.addEventListener("click", function (e) {
            e.preventDefault();

            document.querySelector(".sidebar").classList.toggle("shrink");
            document.querySelector(".sidebar").classList.toggle("show");
        });
    }

    // ------------------------------------------------------- //
    // Search Dropdown Menu
    // ------------------------------------------------------ //

    const searchFormControl = document.getElementById("searchInput");
    const dropdownMenu = document.getElementById("searchDropdownMenu");

    if (searchFormControl && dropdownMenu) {
        searchFormControl.addEventListener("focus", function (e) {
            var dropdownMenus = [].slice.call(
                document.querySelectorAll(".dropdown-menu.show:not(#searchDropdownMenu)")
            );
            dropdownMenus.map(function (dropdownMenu) {
                dropdownMenu.classList.remove("show");
            });

            dropdownMenu.classList.add("d-block");
        });
        document.addEventListener("click", function (e) {
            if (e.target.id == "searchInput" || e.target.closest("#searchDropdownMenu")) {
                dropdownMenu.classList.add("d-block");
            } else {
                dropdownMenu.classList.remove("d-block");
            }
        });
    }

    // ------------------------------------------------------- //
    // Init Tooltips
    // ------------------------------------------------------ //

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

//define getcookie function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



// Function to delete a task from the backend API
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('delete-task-btn')) {
        const taskId = event.target.getAttribute('data-task-id');
        fetch(`/tasks/${taskId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Django CSRF token
            }
        })
            .then(response => {
                if (response.ok) {
                    console.log(`Task ${taskId} deleted successfully.`);
                    fetchUserTasks(); // Refresh tasks after deletion
                } else {
                    console.error(`Failed to delete task ${taskId}.`);
                }
            })
            .catch(error => console.error('Error deleting task:', error));
    }
});

// Function to delete all tasks from the backend API
document.getElementById('delete-all-btn').addEventListener('click', function () {
    fetch('/tasks/delete-all/', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Django CSRF token
        }
    })
        .then(response => {
            if (response.ok) {
                console.log('All tasks deleted successfully.');
                fetchUserTasks(); // Refresh tasks after deletion
            } else {
                console.error('Failed to delete all tasks.');
            }
        })
        .catch(error => console.error('Error deleting all tasks:', error));
});


// Function to fetch task updates from the backend API
function fetchUserTasks() {
    console.log("Fetching user tasks...");
    fetch('/tasks/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('task-container');
            container.innerHTML = '';

            data.forEach(task => {
                const progressColor = task.status === 'FAILURE' ? 'bg-danger' : 'bg-success';

                const card = `
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${task.task_name}</h5>
                            <p>Status: <strong>${task.status}</strong></p>
                            <div class="progress mb-3">
                                <div 
                                    class="progress-bar ${progressColor}" 
                                    role="progressbar" 
                                    style="width: ${task.progress}%" 
                                    aria-valuenow="${task.progress}" 
                                    aria-valuemin="0" 
                                    aria-valuemax="100"
                                >
                                    ${task.progress}%
                                </div>
                            </div>
                            <pre>${task.log_messages ? task.log_messages : ''}</pre>
                            <button class="btn btn-danger delete-btn" data-id="${task.log_id}">Delete</button>
                        </div>
                    </div>
                `;
                container.innerHTML += card;
            });

            // Add event listeners to delete buttons
            document.querySelectorAll('.delete-btn').forEach(button => {
                button.addEventListener('click', function () {
                    const taskId = this.getAttribute('data-id');
                    deleteTask(taskId);
                });
            });
        })
        .catch(error => console.error('Error fetching tasks:', error));
}

// Delete a specific task
function deleteTask(taskId) {
    fetch(`/tasks/${taskId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(response => {
            if (response.ok) {
                console.log(`Task ${taskId} deleted successfully.`);
                fetchUserTasks(); // Refresh task list after deletion
            } else {
                console.error(`Failed to delete task ${taskId}.`);
            }
        })
        .catch(error => console.error('Error deleting task:', error));
}

// Run fetchUserTasks on page load
fetchUserTasks();



//Run the function once when the page loads
fetchUserTasks();
setInterval(fetchUserTasks, 5000); // Fetch tasks every 5 seconds

