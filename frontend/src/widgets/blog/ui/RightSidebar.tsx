import { Avatar, AvatarFallback, AvatarImage } from '@/shared/ui/avatar';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/ui/card';
import { Separator } from '@/shared/ui/separator';
import { Eye, Users } from 'lucide-react';
import { mostReadPosts, topChannels, topics } from '../lib/data';
import { Badge } from '@/shared/ui/badge';

export function RightSidebar() {
  const formatNumber = (num: number) => {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
  };

  return (
    <div className="space-y-6">
      {/* Most Read Posts */}
      <h2 className="text-lg font-semibold mt-4 mb-2">
        Most Read
      </h2>
      <Card className='bg-card/30 py-3'>
        <CardContent className='px-3'>
          <div className="space-y-4">
            {mostReadPosts.map((post, index) => (
              <div key={post.id} className="space-y-2">
                <div className="flex items-start space-x-3">
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium line-clamp-2 hover:text-primary cursor-pointer">
                      {post.title}
                    </h4>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-xs text-muted-foreground">by {post.author}</span>
                      <span className="text-xs text-muted-foreground">•</span>
                      <span className="text-xs text-muted-foreground">{post.readTime}</span>
                    </div>
                    <div className="flex items-center space-x-1 mt-1">
                      <Eye className="h-3 w-3 text-muted-foreground" />
                      <span className="text-xs text-muted-foreground">
                        {formatNumber(post.views)} views
                      </span>
                    </div>
                  </div>
                </div>
                {index < mostReadPosts.length - 1 && <Separator className="mt-3" />}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Top Channels */}
      <h2 className="text-lg font-semibold mt-4 mb-2 flex items-center">
        <Users className="h-5 w-5 mr-2" />
        Top Channels
      </h2>
      <Card className='bg-card/30 py-3'>
        <CardContent className='px-2'>
          <div className="space-y-4">
            {topChannels.map((channel, index) => (
              <div key={channel.id} className="space-y-2">
                <div className="flex items-center space-x-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={channel.avatar} alt={channel.name} />
                    <AvatarFallback>{channel.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium hover:text-primary cursor-pointer">
                      {channel.name}
                    </h4>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-xs text-muted-foreground">
                        {formatNumber(channel.subscribers)} subscribers
                      </span>
                      <span className="text-xs text-muted-foreground">•</span>
                      <span className="text-xs text-muted-foreground">
                        {channel.posts} posts
                      </span>
                    </div>
                  </div>
                </div>
                {index < topChannels.length - 1 && <Separator className="mt-3" />}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <h2 className="text-lg font-semibold mt-4 mb-2 flex items-center">Topics</h2>
      <Card className='bg-card/30 p-3'>
        <CardContent className='px-0'>
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
    </div>
  );
}
