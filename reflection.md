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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
