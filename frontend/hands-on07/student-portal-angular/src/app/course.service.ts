import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

export const courses: Course[] = [
  { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Wireless Communication', code: 'EC3501', credits: 3, grade: 'B+' },
  { id: 3, name: 'Network Security', code: 'CS305', credits: 4, grade: 'A-' },
  { id: 4, name: 'Operating Systems', code: 'CS204', credits: 4, grade: 'B' },
  { id: 5, name: 'Database Systems', code: 'CS210', credits: 3, grade: 'A' }
];

// Task 2, step 96: service is a singleton (providedIn: 'root') that
// centralises data-fetching so components stay free of HTTP code.
@Injectable({
  providedIn: 'root'
})
export class CourseService {
  getCourses(): Observable<Course[]> {
    return of(courses);
  }
}
