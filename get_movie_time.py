from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

def get_movie_time(webpage):
    # the input 'webpage' should be like this:
    # https://tw.movies.yahoo.com/movietime_result.html?id=5645

    # get the movie timetable raw html code
    data = urlopen(webpage).read()
    text = data.split('\n')
    in_text = False
    buf = ''
    for t in text:
        if 'row-container clearfix' in t:
            in_text = True
        if 'class=\"tm\"' in t and in_text:
            buf = '{0}\n</div>'.format(buf)
            break
        if in_text:
            buf = '{0}\n{1}'.format(buf, t)
    soup = BeautifulSoup(buf)

    # get cinema names
    cinema_name = []
    cinema = soup.findAll('a')
    for item in cinema:
        cinema_name.append(item.text)

    # get time table for each cinema
    index = -1
    cinema_time = []
    times = soup.findAll('span')
    for t in times:
        if 'mvtype' in str(t):
            index += 1
            cinema_time.append([])
        else:
            cinema_time[index].append(t.text)

    return dict(zip(cinema_name, cinema_time))
