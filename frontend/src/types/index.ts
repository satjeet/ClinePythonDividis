export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  profile: UserProfile
}

export interface UserProfile {
  experience_points: number
  current_level: number
  created_at: string
  updated_at: string
}

export interface Module {
  id: string
  name: string
  description: string
  icon: string
  order: number
  xp_required: number
  state: 'locked' | 'unlocked' | 'completed'
}

export interface Mission {
  id: string
  module: Module
  title: string
  description: string
  xp_reward: number
  required_level: number
  created_at: string
  state?: 'active' | 'completed' | 'failed'
}

export interface ModuleProgress {
  user: User
  module: Module
  state: 'locked' | 'unlocked' | 'completed'
  experience_points: number
  last_activity: string
}

export interface MissionProgress {
  user: User
  mission: Mission
  state: 'active' | 'completed' | 'failed'
  started_at: string
  completed_at?: string
}

export interface Achievement {
  name: string
  description: string
  icon: string
  xp_reward: number
}

export interface UserAchievement {
  user: User
  achievement: Achievement
  unlocked_at: string
}

export interface Streak {
  user: User
  module: Module
  current_streak: number
  longest_streak: number
  last_activity: string
}
