'use client';

import { Card, CardContent, Typography, Grid, Box } from '@mui/material';
import { 
  Assignment as TaskIcon, 
  Note as NoteIcon,
  CheckCircle as CompletedIcon,
  Schedule as PendingIcon 
} from '@mui/icons-material';

// Mock data - in a real app, this would come from API
const stats = {
  total_tasks: 12,
  completed_tasks: 8,
  pending_tasks: 4,
  total_notes: 25,
  high_priority: 2,
  medium_priority: 2,
  low_priority: 0,
};

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  subtitle?: string;
}

function StatCard({ title, value, icon, color, subtitle }: StatCardProps) {
  return (
    <Card className="h-full">
      <CardContent className="p-6">
        <Box className="flex items-center justify-between mb-2">
          <Box className={`p-3 rounded-full ${color} bg-opacity-20`}>
            {icon}
          </Box>
          <Typography variant="h4" className="font-bold text-white">
            {value}
          </Typography>
        </Box>
        <Typography variant="h6" className="text-white mb-1">
          {title}
        </Typography>
        {subtitle && (
          <Typography variant="body2" className="text-gray-400">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

export function DashboardStats() {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} lg={3}>
        <StatCard
          title="Total Tasks"
          value={stats.total_tasks}
          icon={<TaskIcon className="text-blue-400" />}
          color="text-blue-400"
          subtitle={`${stats.completed_tasks} completed`}
        />
      </Grid>
      
      <Grid item xs={12} sm={6} lg={3}>
        <StatCard
          title="Completed"
          value={stats.completed_tasks}
          icon={<CompletedIcon className="text-green-400" />}
          color="text-green-400"
          subtitle={`${Math.round((stats.completed_tasks / stats.total_tasks) * 100)}% completion rate`}
        />
      </Grid>
      
      <Grid item xs={12} sm={6} lg={3}>
        <StatCard
          title="Pending Tasks"
          value={stats.pending_tasks}
          icon={<PendingIcon className="text-yellow-400" />}
          color="text-yellow-400"
          subtitle={`${stats.high_priority} high priority`}
        />
      </Grid>
      
      <Grid item xs={12} sm={6} lg={3}>
        <StatCard
          title="Total Notes"
          value={stats.total_notes}
          icon={<NoteIcon className="text-purple-400" />}
          color="text-purple-400"
          subtitle="Organized & searchable"
        />
      </Grid>
    </Grid>
  );
}