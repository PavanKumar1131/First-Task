// timer.js - handles task timer functionality
// start, pause, and save time for each task

// store timer intervals and times for each task
let timers = {};
let taskTimes = {};

// initialize timer for a task
function initTimer(taskId, initialTime) {
    taskTimes[taskId] = initialTime || 0;
    updateTimerDisplay(taskId);
}

// format seconds to hh:mm:ss
function formatTime(seconds) {
    let hrs = Math.floor(seconds / 3600);
    let mins = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;
    
    // padding with zeros
    hrs = hrs.toString().padStart(2, '0');
    mins = mins.toString().padStart(2, '0');
    secs = secs.toString().padStart(2, '0');
    
    return hrs + ':' + mins + ':' + secs;
}

// update the timer display on page
function updateTimerDisplay(taskId) {
    let display = document.getElementById('timer-' + taskId);
    if (display) {
        display.textContent = formatTime(taskTimes[taskId]);
    }
}

// start timer for a task
function startTimer(taskId) {
    // don't start if already running
    if (timers[taskId]) {
        return;
    }
    
    // update button
    let btn = document.getElementById('timer-btn-' + taskId);
    if (btn) {
        btn.textContent = 'Pause';
        btn.classList.remove('start');
        btn.classList.add('pause');
    }
    
    // start the interval
    timers[taskId] = setInterval(function() {
        taskTimes[taskId]++;
        updateTimerDisplay(taskId);
    }, 1000);
}

// pause timer and save to server
function pauseTimer(taskId) {
    // clear the interval
    if (timers[taskId]) {
        clearInterval(timers[taskId]);
        timers[taskId] = null;
    }
    
    // update button back to start
    let btn = document.getElementById('timer-btn-' + taskId);
    if (btn) {
        btn.textContent = 'Start';
        btn.classList.remove('pause');
        btn.classList.add('start');
    }
    
    // saving task time after pause
    saveTimeToServer(taskId);
}

// save time to server via API
function saveTimeToServer(taskId) {
    let timeSpent = taskTimes[taskId];
    
    fetch('/task/update-time/' + taskId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ time_spent: timeSpent })
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
        if (data.success) {
            console.log('Time saved for task', taskId);
        }
    })
    .catch(function(error) {
        console.error('Error saving time:', error);
    });
}

// toggle task completion status
function toggleComplete(taskId) {
    fetch('/task/complete/' + taskId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
        // reload page to update ui
        location.reload();
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
}

// save all active timers before page unload
window.addEventListener('beforeunload', function() {
    // pause all running timers and save
    for (var taskId in timers) {
        if (timers[taskId]) {
            clearInterval(timers[taskId]);
            
            // quick save - synchronous not ideal but works
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/task/update-time/' + taskId, false);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ time_spent: taskTimes[taskId] }));
        }
    }
});

// modal functions for add/edit task
function openAddModal() {
    document.getElementById('addTaskModal').classList.add('active');
}

function closeAddModal() {
    document.getElementById('addTaskModal').classList.remove('active');
}

function openEditModal(taskId, title, description, category) {
    document.getElementById('editTaskId').value = taskId;
    document.getElementById('editTitle').value = title;
    document.getElementById('editDescription').value = description;
    document.getElementById('editCategory').value = category;
    document.getElementById('editTaskForm').action = '/task/edit/' + taskId;
    document.getElementById('editTaskModal').classList.add('active');
}

function closeEditModal() {
    document.getElementById('editTaskModal').classList.remove('active');
}

// initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    
    // initialize timers from data attributes
    var taskItems = document.querySelectorAll('.task-item');
    taskItems.forEach(function(item) {
        var taskId = item.dataset.taskId;
        var timeSpent = parseInt(item.dataset.taskTime) || 0;
        if (taskId) {
            initTimer(taskId, timeSpent);
        }
    });
    
    // add task button
    var addBtn = document.getElementById('addTaskBtn');
    if (addBtn) {
        addBtn.addEventListener('click', openAddModal);
    }
    
    // close add modal button
    var closeAddBtn = document.getElementById('closeAddModal');
    if (closeAddBtn) {
        closeAddBtn.addEventListener('click', closeAddModal);
    }
    
    // close edit modal button
    var closeEditBtn = document.getElementById('closeEditModal');
    if (closeEditBtn) {
        closeEditBtn.addEventListener('click', closeEditModal);
    }
    
    // timer buttons - start/pause
    document.querySelectorAll('.js-timer-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var taskId = this.dataset.taskId;
            if (this.classList.contains('start')) {
                startTimer(taskId);
            } else {
                pauseTimer(taskId);
            }
        });
    });
    
    // complete toggle buttons
    document.querySelectorAll('.js-complete-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var taskId = this.dataset.taskId;
            toggleComplete(taskId);
        });
    });
    
    // edit buttons
    document.querySelectorAll('.js-edit-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var taskItem = this.closest('.task-item');
            var taskId = taskItem.dataset.taskId;
            var title = taskItem.dataset.taskTitle;
            var description = taskItem.dataset.taskDescription;
            var category = taskItem.dataset.taskCategory;
            openEditModal(taskId, title, description, category);
        });
    });
    
    // delete form confirmation
    document.querySelectorAll('.js-delete-form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Delete this task?')) {
                e.preventDefault();
            }
        });
    });
    
    // close modal when clicking outside
    document.querySelectorAll('.modal').forEach(function(modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });
});
