<script setup>
// Step 108: props declared with defineProps and rendered in the template.
// `id` is included too so the card can link to its detail route.
const props = defineProps({
  id: { type: Number, required: true },
  name: { type: String, required: true },
  code: { type: String, required: true },
  credits: { type: Number, required: true },
  grade: { type: String, required: true },
  enrolled: { type: Boolean, default: false }
})

const emit = defineEmits(['enroll'])

function handleEnroll() {
  emit('enroll', props.id)
}
</script>

<template>
  <article class="course-card">
    <RouterLink :to="`/courses/${id}`" class="course-card__link">
      <h3>{{ name }}</h3>
      <p class="code">{{ code }}</p>
      <div class="meta">
        <span class="credits">{{ credits }} credits</span>
        <span class="grade">Grade: {{ grade }}</span>
      </div>
    </RouterLink>

    <button
      class="enroll-btn"
      :class="{ enrolled: enrolled }"
      :disabled="enrolled"
      @click="handleEnroll"
    >
      {{ enrolled ? 'Enrolled' : 'Enroll' }}
    </button>
  </article>
</template>

<style scoped>
.course-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 1.25rem;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  background: #fff;
}

.course-card__link {
  color: inherit;
  text-decoration: none;
}

.course-card h3 {
  margin: 0 0 0.25rem;
  font-size: 1.05rem;
  color: #111827;
}

.code {
  margin: 0 0 0.5rem;
  color: #6b7280;
  font-size: 0.85rem;
}

.meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #374151;
}

.enroll-btn {
  align-self: flex-start;
  padding: 0.45rem 1rem;
  border: none;
  border-radius: 6px;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

.enroll-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.enroll-btn.enrolled,
.enroll-btn:disabled {
  background: #d1fae5;
  color: #065f46;
  cursor: default;
}
</style>
