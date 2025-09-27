"use client"
import React, { useState } from 'react';
import { Card, CardContent, CardHeader } from '@/shared/ui/card';
import { Badge } from '@/shared/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/shared/ui/avatar';
import { Button } from '@/shared/ui/button';
import {
    MessageCircle,
    ThumbsUp,
    ThumbsDown,
    Bookmark,
    Eye,
    Share2,
    Clock
} from 'lucide-react';

interface BlogPostProps {
    post: {
        id: number;
        title: string;
        content: string;
        author: {
            name: string;
            avatar: string;
            role: string;
        };
        tags: string[];
        stats: {
            views: number;
            comments: number;
            likes: number;
            dislikes: number;
        };
        publishedAt: string;
        readTime: string;
        isSaved: boolean;
    };
}

export function BlogPost({ post }: BlogPostProps) {
    const [isLiked, setIsLiked] = useState(false);
    const [isDisliked, setIsDisliked] = useState(false);
    const [isSaved, setIsSaved] = useState(post.isSaved);
    const [likeCount, setLikeCount] = useState(post.stats.likes);
    const [dislikeCount, setDislikeCount] = useState(post.stats.dislikes);

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    const formatNumber = (num: number) => {
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'k';
        }
        return num.toString();
    };

    const handleLike = () => {
        if (isDisliked) {
            setIsDisliked(false);
            setDislikeCount(dislikeCount - 1);
        }
        setIsLiked(!isLiked);
        setLikeCount(isLiked ? likeCount - 1 : likeCount + 1);
    };

    const handleDislike = () => {
        if (isLiked) {
            setIsLiked(false);
            setLikeCount(likeCount - 1);
        }
        setIsDisliked(!isDisliked);
        setDislikeCount(isDisliked ? dislikeCount - 1 : dislikeCount + 1);
    };

    const handleSave = () => {
        setIsSaved(!isSaved);
    };

    return (
        <Card className="blog-card-hover">
            <CardHeader>
                {/* Author Info */}
                <div className="flex items-center space-x-3">
                    <Avatar className="h-10 w-10">
                        <AvatarImage src={post.author.avatar} alt={post.author.name} />
                        <AvatarFallback>{post.author.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                        <div className="flex items-center space-x-2">
                            <h3 className="font-semibold text-sm">{post.author.name}</h3>
                            <Badge variant="secondary" className="text-xs">
                                {post.author.role}
                            </Badge>
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                            <Clock className="h-3 w-3" />
                            <span>{formatDate(post.publishedAt)}</span>
                            <span>•</span>
                            <span>{post.readTime}</span>
                        </div>
                    </div>
                </div>

                {/* Post Title */}
                <h2 className="text-xl font-bold my-3 hover:text-primary cursor-pointer">
                    {post.title}
                </h2>

                {/* Post Content Preview */}
                <p className="text-muted-foreground mb-4 line-clamp-3">
                    {post.content}
                </p>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mb-0">
                    {post.tags.map((tag) => (
                        <Badge key={tag} variant="outline" className="text-xs">
                            {tag}
                        </Badge>
                    ))}
                </div>
            </CardHeader>

            <CardContent className="!py-0 !mt-0">
                {/* Stats and Actions */}
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                        {/* View Count */}
                        <div className="flex items-center space-x-1">
                            <Eye className="h-4 w-4" />
                            <span>{formatNumber(post.stats.views)}</span>
                        </div>

                        {/* Comments */}
                        <div className="flex items-center space-x-1">
                            <MessageCircle className="h-4 w-4" />
                            <span>{post.stats.comments}</span>
                        </div>
                    </div>

                    <div className="flex items-center space-x-2">
                        {/* Like/Dislike Buttons */}
                        <div className="flex items-center space-x-1">
                            <Button
                                variant="ghost"
                                size="sm"
                                className={`h-8 px-2 ${isLiked ? 'text-primary' : ''}`}
                                onClick={handleLike}
                            >
                                <ThumbsUp className={`h-4 w-4 mr-1 ${isLiked ? 'fill-current' : ''}`} />
                                <span className="text-xs">{formatNumber(likeCount)}</span>
                            </Button>
                            <Button
                                variant="ghost"
                                size="sm"
                                className={`h-8 px-2 ${isDisliked ? 'text-destructive' : ''}`}
                                onClick={handleDislike}
                            >
                                <ThumbsDown className={`h-4 w-4 mr-1 ${isDisliked ? 'fill-current' : ''}`} />
                                <span className="text-xs">{formatNumber(dislikeCount)}</span>
                            </Button>
                        </div>

                        {/* Save Button */}
                        <Button
                            variant="ghost"
                            size="sm"
                            className={`h-8 px-2 ${isSaved ? 'text-primary' : ''}`}
                            onClick={handleSave}
                        >
                            <Bookmark className={`h-4 w-4 ${isSaved ? 'fill-current' : ''}`} />
                        </Button>

                        {/* Share Button */}
                        <Button variant="ghost" size="sm" className="h-8 px-2">
                            <Share2 className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
