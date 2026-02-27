-- CreateTable
CREATE TABLE "articles" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "source" TEXT NOT NULL,
    "contentSnippet" TEXT NOT NULL DEFAULT '',
    "author" TEXT,
    "publishedAt" DATETIME NOT NULL,
    "crawledAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "language" TEXT NOT NULL DEFAULT 'en',
    "engagementScore" INTEGER NOT NULL DEFAULT 0,
    "relevanceScore" REAL NOT NULL DEFAULT 0,
    "keywordsMatched" TEXT NOT NULL DEFAULT '[]',
    "isRead" BOOLEAN NOT NULL DEFAULT false,
    "isBookmarked" BOOLEAN NOT NULL DEFAULT false,
    "contentHash" TEXT
);

-- CreateTable
CREATE TABLE "related_projects" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "description" TEXT,
    "stars" INTEGER,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "articleId" TEXT NOT NULL,
    CONSTRAINT "related_projects_articleId_fkey" FOREIGN KEY ("articleId") REFERENCES "articles" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "crawl_logs" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "source" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "itemsFound" INTEGER NOT NULL DEFAULT 0,
    "itemsNew" INTEGER NOT NULL DEFAULT 0,
    "errorMsg" TEXT,
    "startedAt" DATETIME NOT NULL,
    "completedAt" DATETIME,
    "durationMs" INTEGER
);

-- CreateTable
CREATE TABLE "keyword_configs" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "keyword" TEXT NOT NULL,
    "language" TEXT NOT NULL DEFAULT 'en',
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "weight" REAL NOT NULL DEFAULT 1.0
);

-- CreateTable
CREATE TABLE "source_configs" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "source" TEXT NOT NULL,
    "isEnabled" BOOLEAN NOT NULL DEFAULT true,
    "crawlInterval" INTEGER NOT NULL DEFAULT 240,
    "lastCrawledAt" DATETIME,
    "apiKey" TEXT,
    "extraConfig" TEXT
);

-- CreateIndex
CREATE UNIQUE INDEX "articles_url_key" ON "articles"("url");

-- CreateIndex
CREATE INDEX "articles_source_idx" ON "articles"("source");

-- CreateIndex
CREATE INDEX "articles_publishedAt_idx" ON "articles"("publishedAt");

-- CreateIndex
CREATE INDEX "articles_relevanceScore_idx" ON "articles"("relevanceScore");

-- CreateIndex
CREATE INDEX "related_projects_articleId_idx" ON "related_projects"("articleId");

-- CreateIndex
CREATE INDEX "crawl_logs_source_idx" ON "crawl_logs"("source");

-- CreateIndex
CREATE INDEX "crawl_logs_startedAt_idx" ON "crawl_logs"("startedAt");

-- CreateIndex
CREATE UNIQUE INDEX "keyword_configs_keyword_key" ON "keyword_configs"("keyword");

-- CreateIndex
CREATE UNIQUE INDEX "source_configs_source_key" ON "source_configs"("source");
