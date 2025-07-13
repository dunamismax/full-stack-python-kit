'use client';

import { Card, CardContent, Typography, Box, Chip, Avatar } from '@mui/material';
import { 
  Task as TaskIcon, 
  Note as NoteIcon,
  CheckCircle as CompletedIcon,
  Edit as EditIcon 
} from '@mui/icons-material';

// Mock data - in a real app, this would come from API
const activities = [
  {
    id: 1,
    type: 'task_completed',
    title: 'Completed "Setup database models"',
    time: '2 minutes ago',
    icon: <CompletedIcon className="text-green-400" />,
    color: 'success',
  },
  {
    id: 2,
    type: 'note_created',
    title: 'Created note "API Design Patterns"',
    time: '15 minutes ago',
    icon: <NoteIcon className="text-blue-400" />,
    color: 'primary',
  },
  {
    id: 3,
    type: 'task_created',
    title: 'Added task "Implement authentication"',
    time: '1 hour ago',
    icon: <TaskIcon className="text-purple-400" />,
    color: 'secondary',
  },
  {
    id: 4,
    type: 'note_updated',
    title: 'Updated note "Development Guidelines"',
    time: '2 hours ago',
    icon: <EditIcon className="text-yellow-400" />,
    color: 'warning',
  },
  {
    id: 5,
    type: 'task_completed',
    title: 'Completed "Setup FastAPI backend"',
    time: '3 hours ago',
    icon: <CompletedIcon className="text-green-400" />,
    color: 'success',
  },
];

export function RecentActivity() {
  return (
    <Card>
      <CardContent className="p-6">
        <Typography variant="h6" className="mb-4 text-white font-semibold">
          Recent Activity
        </Typography>
        
        <Box className="space-y-4">
          {activities.map((activity) => (
            <Box key={activity.id} className="flex items-start space-x-3">
              <Avatar className="bg-dark-700 w-10 h-10">
                {activity.icon}
              </Avatar>
              
              <Box className="flex-1 min-w-0">
                <Typography variant="body1" className="text-white font-medium">
                  {activity.title}
                </Typography>
                <Typography variant="body2" className="text-gray-400">
                  {activity.time}
                </Typography>
              </Box>
              
              <Chip
                label={activity.type.replace('_', ' ')}
                size="small"
                color={activity.color as any}
                variant="outlined"
                className="text-xs"
              />
            </Box>
          ))}
          
          {activities.length === 0 && (
            <Box className="text-center py-8">
              <Typography variant="body2" className="text-gray-400">
                No recent activity
              </Typography>
            </Box>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}