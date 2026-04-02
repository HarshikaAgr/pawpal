# PawPal+ Project Reflection

## 1. System Design

- The user should be able to enter basic information about themselves and their pet, like the owner’s name, the pet’s name, and the type of pet.
- The user should be able to add and manage pet care tasks, such as walks, feeding, medicine, grooming, or playtime, along with how long each task takes and how important it is (priority).
- The user should be able to generate and view a daily care plan that picks the most important tasks based on the time available and explains why those tasks were chosen.

**a. Initial design**

Four classes with clear responsibilities:
- **Owner**: Stores user info (name, available time, preferences). Methods let users update preferences and time.
- **Pet**: Stores pet details (name, species, age). Methods to get and update pet info.
- **Task**: Represents a care task (feed, walk, etc.). Has title, duration, priority, category. Methods to update, mark complete, and get details.
- **Scheduler**: Takes a list of tasks and available time. Generates optimized daily plan by sorting tasks by priority and checking time fit. Explains why tasks were chosen.

Relationships: Owner owns Pets, Owner uses Scheduler, Scheduler manages Tasks for Pets.

**b. Design changes**

Yes. Two key changes:
1. **Task → Pet link**: Added `pet: Optional[Pet]` attribute so tasks know which pet they belong to.
2. **Scheduler → Owner reference**: Changed Scheduler to accept `owner: Owner` instead of separate task/time lists. Scheduler now calls `owner.get_all_tasks()` to retrieve all pet tasks. This is cleaner and ties the scheduler to the data source.

Why: Tighter encapsulation. Tasks know their pet. Scheduler knows its owner. Makes the system less rigid and easier to extend.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers three main constraints:
1. **Available time**: Can't schedule more tasks than owner has time for
2. **Task priority**: High priority tasks scheduled first, then medium, then low
3. **Task duration**: Each task has a required duration in minutes

Decision: Priority mattered most because pet owners want to ensure critical tasks (feeding, medicine) happen before nice-to-haves (playtime). Time was checked after sorting by priority.

**b. Tradeoffs**

My scheduler makes one major tradeoff:
- **Greedy scheduling**: Schedule tasks in priority order, fitting as many as possible. Don't rearrange already-scheduled tasks to fit more tasks overall.

Example: If I have 60 minutes and tasks are:
- Feed (5 min, high) ✓ Scheduled
- Walk (30 min, high) ✓ Scheduled
- Play (20 min, medium) ✓ Scheduled
- Groom (10 min, low) ✗ Doesn't fit because 5 + 30 + 20 = 55, so only 5 minutes 

Why reasonable?
- **Simplicity**: Easy to understand - just go down the list and fit what you can
- **Fairness**: High-priority tasks always get in first (guaranteed)
- **Speed**: No complex optimization needed (good for a beginner project!)
- **Practical**: Pet owners prefer simple schedules they can understand

Alternative (not chosen): "Bin packing" algorithm to rearrange tasks and fit more overall. But this is complex and could surprise users.

Second tradeoff - **Conflict detection**:
- **Exact time matching only**: Only warns if two tasks start at EXACTLY the same time (08:00). Doesn't check if they overlap in duration (task runs 08:00-08:20, another 08:15-08:30).

Why reasonable?
- **Simple to understand**: Owner looks at times and can see conflicts immediately
- **Practical**: Most pet tasks have discrete start times, not overlapping durations
- **Beginner-friendly**: Not over-engineering for edge cases
- **Safe**: Better to warn too much than miss a real conflict

---

## 3. AI Collaboration

**a. How you used AI**

Three key ways AI helped:

1. **Code Generation + Understanding**: AI wrote the some of the methods that I was having difficulty writing, but I READ and UNDERSTOOD the code instead of copy-pasting. This way I was able to learn HOW the code works, not just WHAT it does.

2. **Debugging Suggestions**: When code didn't work as expected, AI helped me:
   - Trace through logic step-by-step (recurring task creation)
   - Understand WHY session state wasn't persisting in Streamlit
   - Fix conflict detection to check the right conditions
   - Verify that `owner.get_all_tasks()` flattened all pet tasks correctly

3. **Architecture Questions**: Most helpful prompts were questions, not requests:
   - "How should Scheduler retrieve all tasks from Owner's pets?" → Led to cleaner design
   - "Is this conflict detection correct?" → Caught edge cases
   - "What tradeoffs am I making here?" → Forced critical thinking

**What worked best for me:** 

AI helped most when I asked it to explain ideas and debug problems, instead of just asking it to generate code.

**Edge cases AI helped catch:**
- Empty task list = scheduler should warn, not crash ✓
- Recurring task without pet = should still work ✓
- Session state reset between Streamlit button clicks = use st.session_state ✓

**How separate chat sessions helped me stay organized:**

Using separate AI chat sessions for design, implementation, testing, and reflection helped me stay organized because each conversation stayed focused on one goal. It reduced confusion, made the AI responses more relevant, and helped me separate brainstorming from debugging and final writing. That made it easier to keep the system design clean and avoid mixing unrelated changes together.

**b. Judgment and verification**

**What I rejected:**

AI suggested complex session state for app.py:
```python
# AI version - complex
st.session_state.owner_name = ...
st.session_state.owner_time = ...
st.session_state.current_pet = ...
# etc... (too many separate variables)
```

I chose: Store the Owner object directly
```python
# My version - simple
st.session_state.owner = Owner(name, available_time)
# One variable, all data in Owner
```

**Why I rejected it:**
- Multiple variables = hard to keep in sync
- One Owner object = cleaner, easier to manage
- App logic is simpler (pass `st.session_state.owner` to Scheduler)

**How I verified:**
- Tested "Create Owner" button → owner saved in session 
- Tested "Add Pet" button → pets added to owner via `owner.add_pet()` 
- Tested "Generate Schedule" button → scheduler accessed owner data correctly 
- Streamlit UI worked smoothly with no state sync issues 

**Lesson:** Simple is better. Don't overcomplicate just because you *can*.

---

## 4. Testing and Verification

**a. What you tested**

I tested eight important behaviors in the system:

1. **Task Completion**: `mark_complete()` changes a task's status to completed  
2. **Pet Task Management**: Adding tasks to a pet increases that pet’s task count  
3. **Owner Pet Management**: Adding a pet to an owner increases the owner’s pet count  
4. **Schedule Generation**: The scheduler creates a plan when tasks fit in the available time  
5. **Sorting by Time**: Tasks are returned in chronological order  
6. **Recurring Auto-Creation**: Completing a daily task creates the next task for tomorrow  
7. **Conflict Detection**: Two tasks at the same start time produce a conflict warning  
8. **No-Fit Edge Case**: If available time is too small, the plan is empty instead of crashing  

Why important:
- These tests cover both normal behavior and edge cases
- They verify the core scheduling logic
- They confirm that recurring tasks and conflicts work correctly
- They help show that the app logic is reliable before connecting it to the UI

**b. Confidence**

**Confidence level: 4/5 stars**

Working well:
- Core scheduling logic tested
- Recurring tasks demo'd in main.py
- UI wired and functional
- Core methods are documented with docstrings

Could test more:
- Edge case: 0 available minutes (can't fit any task)
- Edge case: 100 tasks (performance)
- Edge case: Circular dependencies (task depends on another task)
- Weekly task math (does +7 days work across months/years?)

---

## 5. Reflection

**a. What went well**

Most satisfied with: **The recurring task automation with timedelta**

Why:
- Solves a real problem (pet owners repeat tasks daily!)
- Clean implementation: `task.get_next_due_date()` + `Pet.complete_task()`
- Auto-creates next occurrence → no manual work
- Date math makes sense to beginners

**b. What you would improve**

If I had another iteration:

1. **Better UI sorting**: Let users pick between 3 sorting strategies (not dropdown, actual filters)
2. **Task categories dropdown**: Instead of free text, restrict to ["feeding", "exercise", "grooming", "medicine", "play"]
3. **Recurring task editing**: Let users change daily task to weekly without deleting
4. **Mobile-responsive**: Current Streamlit works but mobile could be better
5. **Timezone support**: Due dates assume same timezone (needed for multi-user)

**c. Key takeaway**

**Being the "lead architect" means:** You, not the AI, make the final design decisions.

What I learned:
- AI is great at implementing specs, not deciding specs
- When AI suggests something, ask: "Does this fit my design? Is it simpler or more complex?"
- Stay focused on requirements. Reject features that sound cool but aren't needed
- Document your reasoning (tradeoffs, constraints) so you can explain "why" later

**Best principle:** Use AI as a fast coder, not as the designer. You decide what gets built. AI decides how to build it efficiently.


