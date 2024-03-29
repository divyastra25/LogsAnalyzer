import akka.http.scaladsl.model.{HttpEntity, HttpRequest, HttpResponse}
import akka.http.scaladsl.Http
import akka.actor.typed.ActorSystem
import akka.actor.typed.scaladsl.Behaviors
import com.typesafe.config.ConfigFactory
import org.slf4j.{Logger, LoggerFactory}

import scala.concurrent.Await
import scala.concurrent.duration.DurationInt
import scala.concurrent.{ExecutionContextExecutor, Future}
package akkaHttp {
  object httpClient {
    implicit val system: ActorSystem[Nothing] = ActorSystem(Behaviors.empty, "SingleRequest")
    implicit val executionContext: ExecutionContextExecutor = system.executionContext

    // logger for logging progression of request
    val logger: Logger = LoggerFactory.getLogger(classOf[httpClient.type])

    def sendRequest(date: String, start: String, delta: String): Future[String] = {
      // sends HTTP request to API Gateway and waits for HttpResponse
      val responseFuture: Future[HttpResponse] = Http().singleRequest(HttpRequest(uri = s"https://qggew40x1g.execute-api.us-east-2.amazonaws.com/demo/logs?start=$start&delta=$delta&date=$date"))
      logger.info("HTTP Request Sent!")

      // returns data structure containing payload
      val entityFuture: Future[HttpEntity.Strict] = responseFuture.flatMap(response => {
        logger.info("Response Received!")
        response.entity.toStrict(2.seconds)
      })

      // extract data we need
      entityFuture.map(entity => entity.data.utf8String)
    }

    def main(args: Array[String]): Unit = {
      logger.info("Client Started")
      val confFile = ConfigFactory.load()  // load "application.conf" config file
      val params = confFile.getConfig("client")
      logger.info("Config File Loaded")

      val data = Await.result(sendRequest(params.getString("date"), params.getString("start"), params.getString("delta")), 5.seconds)
      println(s"Response Data: $data")
      logger.info("Results Printed")
      system.terminate()  // terminating the process for client

    }
  }
}
