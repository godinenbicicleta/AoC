package day04

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"
)

const (
	wakeUp = "wake up"
	sleep  = "sleep"
	begin  = "begin"
)

type RawRecord struct {
	year   int
	month  int
	day    int
	hour   int
	minute int
	text   string
}

type Record struct {
	timestamp time.Time
	guard     int
	action    string
}

func SortRecords(records []RawRecord) {
	sort.Slice(records, func(i, j int) bool {
		if records[i].year != records[j].year {
			return records[i].year < records[j].year
		}
		if records[i].month != records[j].month {
			return records[i].month < records[j].month
		}
		if records[i].day != records[j].day {
			return records[i].day < records[j].day
		}
		if records[i].hour != records[j].hour {
			return records[i].hour < records[j].hour
		}
		if records[i].minute != records[j].minute {
			return records[i].minute < records[j].minute
		}
		return false
	})
}

func ParseRecord(line string) RawRecord {
	var year, month, day, hour, minute int
	start := strings.Index(line, "[") + 1
	end := strings.Index(line, "]")
	text := line[end+2:]
	_, err := fmt.Sscanf(line[start:end], "%d-%d-%d %d:%d", &year, &month, &day, &hour, &minute)
	if err != nil {
		panic(err)
	}
	return RawRecord{year: year, month: month, day: day, hour: hour, minute: minute, text: text}
}

func Solve(fname string) (int, int) {
	file, err := os.Open(fname)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	rawRecords := []RawRecord{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		record := ParseRecord(line)
		rawRecords = append(rawRecords, record)
	}
	SortRecords(rawRecords)

	records := Parse(rawRecords)

	timeAsleep := make(map[int]int)
	prevs := make(map[int]Record)
	sleepMinutes := make(map[int]map[int]int)

	for _, record := range records {
		guard := record.guard
		prev, ok := prevs[guard]
		if !ok {
			prevs[guard] = record
			continue
		}
		if prev.action == sleep && record.action == wakeUp {
			timeAsleep[guard] += int(record.timestamp.Sub(prev.timestamp).Seconds())
			for minute := prev.timestamp.Minute(); minute < record.timestamp.Minute(); minute++ {
				if sleepMinutes[guard] == nil {
					sleepMinutes[guard] = make(map[int]int)
				}
				sleepMinutes[guard][minute]++
			}

		}
		prevs[guard] = record
	}

	maxAsleep := 0
	maxGuard := 0
	for guard, timeSleeping := range timeAsleep {
		if timeSleeping > maxAsleep {
			maxAsleep = timeSleeping
			maxGuard = guard
		}
	}

	maxCount := -1
	maxMinute := -1
	for minute, count := range sleepMinutes[maxGuard] {
		if count > maxCount {
			maxMinute = minute
			maxCount = count
		}

	}

	maxSleep := -1
	maxSleepGuard := -1
	maxMinuteSleep := -1
	for g, m := range sleepMinutes {
		for minute, count := range m {
			if count > maxSleep {
				maxSleep = count
				maxSleepGuard = g
				maxMinuteSleep = minute
			}
		}
	}

	return maxMinute * maxGuard, maxMinuteSleep * maxSleepGuard
}

func Parse(rawRecords []RawRecord) []Record {
	records := []Record{}
	re := regexp.MustCompile(`\d+`)
	gid := -1
	for _, rawRecord := range rawRecords {
		ts := time.Date(rawRecord.year, time.Month(rawRecord.month), rawRecord.day, rawRecord.hour, rawRecord.minute, 0, 0, time.UTC)
		action := wakeUp
		if stringId := re.FindString(rawRecord.text); stringId != "" {
			guardId, err := strconv.Atoi(stringId)
			if err != nil {
				panic(err)
			}
			gid = guardId
			action = begin
		} else if strings.Contains(rawRecord.text, "asleep") {
			action = sleep
		}

		record := Record{timestamp: ts, guard: gid, action: action}
		records = append(records, record)
	}
	return records
}
