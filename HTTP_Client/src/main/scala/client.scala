import akka.http.scaladsl.model.{HttpEntity, HttpRequest, HttpResponse}
import akka.http.scaladsl.Http
import akka.actor.typed.ActorSystem
import akka.actor.typed.scaladsl.Behaviors

import scala.concurrent.duration.DurationInt

import scala.concurrent.Future

object http_client {
  implicit val system = ActorSystem(Behaviors.empty, "SingleRequest")
  implicit val executionContext = system.executionContext

  def sendRequest() = {
    val responseFuture: Future[HttpResponse] = Http().singleRequest(HttpRequest(uri = "https://qnvqyz4nka.execute-api.us-east-2.amazonaws.com/test/indexes?start=08:16:46&delta=00:00:24"))
    val entityFuture: Future[HttpEntity.Strict] = responseFuture.flatMap(response => response.entity.toStrict(2.seconds))
    entityFuture.map(entity => entity.data.utf8String)
  }

  def main(args: Array[String]): Unit = {
    sendRequest().foreach(println)
  }
}
