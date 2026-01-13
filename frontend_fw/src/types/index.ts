// User Types
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'organizer' | 'treasurer' | 'participant';
  is_active: boolean;
  profile?: UserProfile;
}

export interface UserProfile {
  id: number;
  user: number;
  phone_number?: string;
  bio?: string;
  avatar?: string;
  department?: string;
  student_id?: string;
  year_of_graduation?: number;
}

// Auth Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role?: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  access: string;
  refresh: string;
}

// Timeline Types
export interface Timeline {
  id: number;
  title: string;
  description: string;
  category: 'pre_event' | 'main_event' | 'post_event' | 'other';
  start_date: string;
  end_date?: string;
  is_published: boolean;
  is_featured: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
  events?: TimelineEvent[];
}

export interface TimelineEvent {
  id: number;
  timeline: number;
  title: string;
  description: string;
  event_date: string;
  location?: string;
  image?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

// Responsibility Types
export interface Responsibility {
  id: number;
  title: string;
  description: string;
  category?: number;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'pending' | 'in_progress' | 'completed' | 'on_hold';
  due_date?: string;
  assigned_to?: number;
  assigned_to_details?: User;
  created_by: number;
  created_by_details?: User;
  created_at: string;
  updated_at: string;
}

export interface ResponsibilityCategory {
  id: number;
  name: string;
  description?: string;
  color?: string;
}

// API Response Types
export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}
