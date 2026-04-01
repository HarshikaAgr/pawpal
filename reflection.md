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
- Walk (20 min, high) ✓ Scheduled
- Groom (30 min, medium) ✗ Doesn't fit (5+20+30 = 55, but we have 60... wait, this WOULD fit!)

Actually, better example:
- Feed (5 min, high) ✓ Scheduled
- Walk (30 min, high) ✓ Scheduled
- Play (20 min, medium) ✓ Scheduled
- Groom (10 min, low) ✗ Doesn't fit (5+30+20 = 55, leaves only 5 min)

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

1. **Code Generation (Agent Mode)**: Scaffolded all 40+ methods in one task. Faster than writing by hand, freed time for testing.
2. **Docstring Enhancement**: AI suggested clearer docstrings with return types and examples. Made code beginner-friendly.
3. **Algorithm Evaluation**: Compared simple vs pythonic versions. Helped decide when complexity is worth it (it wasn't for this project).

Most helpful prompts:
- "Implement Task, Pet, Owner, Scheduler with these specs..."
- "How should Scheduler retrieve all tasks from Owner's pets?"
- "Simplify this conflict detection for readability"

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

Tested four core behaviors:

1. **Task Completion**: Mark task done → `completed = True` 
2. **Pet Task Management**: Add task to pet → increases task count 
3. **Recurring Auto-Creation**: Complete daily task → new task created for tomorrow 
4. **Conflict Detection**: Two tasks @ 08:00 → warning displayed (no crash) 

Why important:
- Task completion is fundamental to the whole system
- Recurring tasks are the "smart" feature
- Conflicts must warn but not break the app

**b. Confidence**

**Confidence level: 4/5 stars**

Working well:
- Core scheduling logic tested
- Recurring tasks demo'd in main.py
- UI wired and functional
- All 40+ methods have docstrings

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


