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

// Function to fetch task updates from the backend API
function fetchUserTasks() {
    console.log("fetchUserTasks is running...");
    fetch('/tasks/')
        .then(response => response.json())
        .then(data => {
            console.log("Data fetched from API:", data);

            const container = document.getElementById('task-container');
            if (!container) {
                console.error("Task container not found!");
                return;
            }

            container.innerHTML = ''; // Clear previous tasks
            if (data.length === 0) {
                console.log("No tasks to display.");
                container.innerHTML = '<p>No tasks found.</p>';
                return;
            }

            data.forEach(task => {
                console.log("Processing task:", task);
                const progressColor = task.status === 'FAILURE' ? 'bg-danger' : 'bg-success';

                const card = `
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${task.task_name}</h5>
                            <p><strong>Status:</strong> ${task.status}</p>
                            <div class="progress mb-3">
                                <div 
                                    class="progress-bar ${progressColor}" 
                                    role="progressbar" 
                                    style="width: ${task.progress}%" 
                                    aria-valuenow="${task.progress}" 
                                    aria-valuemin="0" 
                                    aria-valuemax="100"
                                >
                                    ${task.status === 'IN_PROGRESS' ? `${task.progress}%` : task.status}
                                </div>
                            </div>
                            ${task.result ? `<p><strong>Result:</strong> ${task.result}</p>` : ''}
                            ${task.error_message ? `<p class="text-danger"><strong>Error:</strong> ${task.error_message}</p>` : ''}
                        </div>
                    </div>
                `;
                container.innerHTML += card; // Append the card
            });
        })
        .catch(error => {
            console.error("Error fetching tasks:", error);
            const container = document.getElementById('task-container');
            container.innerHTML = '<p class="text-danger">Failed to load tasks. Please try again later.</p>';
        });
}

//Run the function once when the page loads
fetchUserTasks();
setInterval(fetchUserTasks, 5000); // Fetch tasks every 5 seconds