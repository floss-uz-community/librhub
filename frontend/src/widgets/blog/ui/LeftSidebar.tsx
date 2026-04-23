import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/ui/card';
import { Badge } from '@/shared/ui/badge';
import { Separator } from '@/shared/ui/separator';
import { topics, categories } from '../lib/data';

export function LeftSidebar() {
  return (
    <div className="space-y-6">
      {/* Topics Section */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Topics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {topics.map((topic) => (
              <Badge
                key={topic}
                variant="secondary"
                className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
              >
                {topic}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      <Separator />

      {/* Categories Section */}
      <CardTitle className="text-lg font-semibold">Categories</CardTitle>
      <div className="space-y-3">
        {categories.map((category) => (
          <div
            key={category.name}
            className="flex items-center justify-between cursor-pointer hover:bg-muted/50 p-2 rounded-md transition-colors"
          >
            <span className="text-sm font-medium">{category.name}</span>
            <Badge variant="outline" className="text-xs">
              {category.count}
            </Badge>
          </div>
        ))}
      </div>
    </div>
  );
}
